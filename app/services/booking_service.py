from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, BackgroundTasks
from jose import jwt
from app.core.config import settings
from app.models.booking import Booking, BookingStatus
from app.models.event import Event
from app.models.user import User
from app.services.qr import generate_qr_code
from app.services.email import send_email
from app.utils.email_templates import ticket_email_html

def _create_ticket_token(booking_id: int, event_id: int, user_email: str) -> str:
    exp = datetime.now(tz=timezone.utc) + timedelta(days=365)
    payload = {"sub": "ticket", "booking_id": booking_id, "event_id": event_id, "email": user_email, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)

def book_seat(db: Session, user: User, event_id: int, seat_number: int, tasks: BackgroundTasks) -> Booking:
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if seat_number < 1 or seat_number > event.total_seats:
        raise HTTPException(status_code=400, detail="Invalid seat number")

    booking = Booking(user_id=user.id, event_id=event_id, seat_number=seat_number, status=BookingStatus.CONFIRMED,
                      ticket_token="")  # fill after commit

    db.add(booking)
    try:
        db.commit()            
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Seat already booked")

    db.refresh(booking)

  
    ticket_token = _create_ticket_token(booking.id, event_id, user.email)
    verify_url = f"{settings.BASE_URL}/tickets/verify?token={ticket_token}"


    qr_path = generate_qr_code(verify_url, f"booking_{booking.id}")

    
    booking.ticket_token = ticket_token
    booking.qr_path = qr_path
    db.add(booking)
    db.commit()
    db.refresh(booking)

   
    html = ticket_email_html(event.title, seat_number, verify_url)
    tasks.add_task(send_email, user.email, f"Your Ticket: {event.title}", html)

    return booking


def get_user_bookings(db: Session, user_id: int) -> list[Booking]:
    """Get all bookings for a specific user"""
    return db.query(Booking).filter(Booking.user_id == user_id).all()


def cancel_booking(db: Session, booking_id: int, user_id: int) -> Booking:
    """Cancel a booking"""
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id
    ).first()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    
    booking.status = BookingStatus.CANCELLED
    db.commit()
    db.refresh(booking)
    
    return booking



