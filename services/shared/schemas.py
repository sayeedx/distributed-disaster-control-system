from datetime import datetime

from pydantic import BaseModel, Field

from services.shared.enums import DispatchStatus, EventStatus, EventType, UnitStatus, UnitType


class UnitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    unit_type: UnitType
    location_x: float
    location_y: float


class UnitRead(BaseModel):
    id: int
    name: str
    unit_type: UnitType
    status: UnitStatus
    location_x: float
    location_y: float
    last_heartbeat: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class EventCreate(BaseModel):
    event_type: EventType
    severity: int = Field(ge=1, le=5)
    location_x: float
    location_y: float


class EventRead(BaseModel):
    id: int
    event_type: EventType
    severity: int
    location_x: float
    location_y: float
    status: EventStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class DispatchRead(BaseModel):
    id: int
    event_id: int
    unit_id: int
    status: DispatchStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
