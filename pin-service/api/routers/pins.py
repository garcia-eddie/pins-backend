from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import db_pin
from ..database.database import get_db
from ..schemas.schema_pin import CreatePinRequest, PinResponse


router = APIRouter(
    prefix="/pins",
    tags=["pins"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=PinResponse)
def create_pin(pin: CreatePinRequest, db: Session = Depends(get_db)):
    rs = db_pin.create_pin(db, pin)
    response = PinResponse.from_orm(rs)
    return response


@router.get("/", response_model=List[PinResponse])
def get_pins(db: Session = Depends(get_db)):
    rs = db_pin.get_all_pins(db)
    response = [PinResponse.from_orm(res) for res in rs]
    return response
