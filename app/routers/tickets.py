from fastapi import APIRouter, HTTPException, Query, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.deps import get_db
from app.models.booking import Booking

router = APIRouter(prefix="/api/tickets", tags=["Tickets"])

@router.get("/verify")
def verify_ticket(
    token: str = Query(..., description="Signed ticket JWT token"),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        booking_id = payload.get("booking_id")
        if booking_id is None:
            raise HTTPException(status_code=400, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired ticket")

    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    return {
        "valid": True,
        "booking_id": booking.id,
        "event_id": booking.event_id,
        "email": payload.get("email"),
    }