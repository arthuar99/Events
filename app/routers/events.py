from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db, get_current_user
from app.schemas.event import EventCreate, EventOut
from app.models.event import Event
from app.models.user import User
from typing import List

router = APIRouter(prefix="/api/events", tags=["Events"])

@router.post("", response_model=EventOut)
def create_event(payload: EventCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    event = Event(**payload.model_dump(), created_by_id=user.id)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.get("", response_model=List[EventOut])
def list_events(db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.starts_at).all()

