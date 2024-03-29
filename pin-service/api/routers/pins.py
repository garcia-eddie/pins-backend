from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas, crud


router = APIRouter(
    prefix="/pins",
    tags=["pins"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=schemas.Pin)
def create_pin(pin: schemas.PinBase, db: Session = Depends(get_db)):
    rs = crud.create_pin(db, pin)
    response = schemas.Pin.from_orm(rs)
    return response


@router.get("/", response_model=List[schemas.Pin])
def get_pins(db: Session = Depends(get_db)):
    rs = crud.get_all_pins(db)
    response = [schemas.Pin.from_orm(res) for res in rs]
    return response
