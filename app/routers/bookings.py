from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.booking import BookingCreate, BookingOut
from app.services.booking_service import book_seat
from app.models.user import User
from app.models.booking import Booking
from typing import List

# Router for event-specific bookings
router = APIRouter(prefix="/api/events/{event_id}/bookings", tags=["Bookings"])

@router.post("", response_model=BookingOut)
def create_booking(event_id: int, payload: BookingCreate, tasks: BackgroundTasks,
                   db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    booking = book_seat(db, user, event_id, payload.seat_number, tasks)
    return booking

# Router for user's general bookings
bookings_router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

@bookings_router.get("", response_model=List[BookingOut])
def get_user_bookings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Get all bookings for the current user"""
    bookings = db.query(Booking).filter(Booking.user_id == user.id).all()
    return bookings

@bookings_router.post("/{booking_id}/cancel")
def cancel_booking(booking_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Cancel a specific booking"""
    booking = db.query(Booking).filter(Booking.id == booking_id, Booking.user_id == user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status == "CANCELLED":
        raise HTTPException(status_code=400, detail="Booking is already cancelled")
    
    booking.status = "CANCELLED"
    db.commit()
    db.refresh(booking)
    
    return {"message": "Booking cancelled successfully"}

