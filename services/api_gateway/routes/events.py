from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from services.shared.db import get_db
from services.shared.messaging import EVENTS_QUEUE, RabbitPublisher
from services.shared.models import Event
from services.shared.schemas import EventCreate, EventRead

router = APIRouter()


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)

    publisher = RabbitPublisher()
    publisher.publish(
        EVENTS_QUEUE,
        {
            "event_id": event.id,
            "event_type": event.event_type.value,
            "severity": event.severity,
            "location_x": event.location_x,
            "location_y": event.location_y,
            "status": event.status.value,
            "created_at": event.created_at.isoformat(),
        },
    )
    return event


@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)) -> list[Event]:
    return db.query(Event).order_by(Event.created_at.desc()).all()


@router.get("/{event_id}", response_model=EventRead)
def get_event(event_id: int, db: Session = Depends(get_db)) -> Event:
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
