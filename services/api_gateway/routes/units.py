from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from services.shared.db import get_db
from services.shared.models import Unit
from services.shared.schemas import UnitCreate, UnitRead

router = APIRouter()


@router.post("/register", response_model=UnitRead, status_code=status.HTTP_201_CREATED)
def register_unit(payload: UnitCreate, db: Session = Depends(get_db)) -> Unit:
    existing = db.query(Unit).filter(Unit.name == payload.name).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="Unit name already exists")

    unit = Unit(**payload.model_dump())
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


@router.get("", response_model=list[UnitRead])
def list_units(db: Session = Depends(get_db)) -> list[Unit]:
    return db.query(Unit).order_by(Unit.created_at.desc()).all()


@router.post("/{unit_id}/heartbeat", response_model=UnitRead)
def heartbeat(unit_id: int, db: Session = Depends(get_db)) -> Unit:
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")

    unit.last_heartbeat = datetime.utcnow()
    db.commit()
    db.refresh(unit)
    return unit
