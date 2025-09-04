from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: str | None = None
    venue: str | None = None
    starts_at: datetime
    ends_at: datetime
    total_seats: int

class EventOut(BaseModel):
    id: int
    title: str
    venue: str | None
    starts_at: datetime
    ends_at: datetime
    total_seats: int
    class Config:
        from_attributes = True
