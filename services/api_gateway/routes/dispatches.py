from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from services.shared.db import get_db
from services.shared.models import Dispatch
from services.shared.schemas import DispatchRead

router = APIRouter()


@router.get("", response_model=list[DispatchRead])
def list_dispatches(db: Session = Depends(get_db)) -> list[Dispatch]:
    return db.query(Dispatch).order_by(Dispatch.created_at.desc()).all()
