from enum import Enum
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey, Enum as SqlEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base

class BookingStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (UniqueConstraint("event_id", "seat_number", name="uq_event_seat"),)

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), index=True)
    seat_number: Mapped[int]
    status: Mapped[BookingStatus] = mapped_column(SqlEnum(BookingStatus), default=BookingStatus.CONFIRMED)
    ticket_token: Mapped[str] = mapped_column(String(512))   
    qr_path: Mapped[str | None] = mapped_column(String(300), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user = relationship("User")
    event = relationship("Event")
