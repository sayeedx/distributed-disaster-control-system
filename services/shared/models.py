from datetime import datetime

from sqlalchemy import DateTime, Enum as SqlEnum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from services.shared.db import Base
from services.shared.enums import (
    DispatchStatus,
    EventStatus,
    EventType,
    UnitStatus,
    UnitType,
)


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    unit_type: Mapped[UnitType] = mapped_column(SqlEnum(UnitType), nullable=False)
    status: Mapped[UnitStatus] = mapped_column(
        SqlEnum(UnitStatus), nullable=False, default=UnitStatus.AVAILABLE
    )
    location_x: Mapped[float] = mapped_column(Float, nullable=False)
    location_y: Mapped[float] = mapped_column(Float, nullable=False)
    last_heartbeat: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_type: Mapped[EventType] = mapped_column(SqlEnum(EventType), nullable=False)
    severity: Mapped[int] = mapped_column(Integer, nullable=False)
    location_x: Mapped[float] = mapped_column(Float, nullable=False)
    location_y: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[EventStatus] = mapped_column(
        SqlEnum(EventStatus), nullable=False, default=EventStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


class Dispatch(Base):
    __tablename__ = "dispatches"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)
    status: Mapped[DispatchStatus] = mapped_column(
        SqlEnum(DispatchStatus), nullable=False, default=DispatchStatus.REQUESTED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
