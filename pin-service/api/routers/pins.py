from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas
from ..database import db_pin
from ..database.database import get_db


router = APIRouter(
    prefix="/pins",
    tags=["pins"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=schemas.Pin)
def create_pin(pin: schemas.PinBase, db: Session = Depends(get_db)):
    rs = db_pin.create_pin(db, pin)
    response = schemas.Pin.from_orm(rs)
    return response


@router.get("/", response_model=List[schemas.Pin])
def get_pins(db: Session = Depends(get_db)):
    rs = db_pin.get_all_pins(db)
    response = [schemas.Pin.from_orm(res) for res in rs]
    return response
