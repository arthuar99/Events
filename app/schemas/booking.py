from pydantic import BaseModel

class BookingCreate(BaseModel):
    seat_number: int

class BookingOut(BaseModel):
    id: int
    event_id: int
    seat_number: int
    status: str
    qr_path: str | None
    class Config:
        from_attributes = True
