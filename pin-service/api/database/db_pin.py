from geoalchemy2 import WKTElement
from sqlalchemy.orm import Session
from typing import List
from .models import Pin
from ..schemas import PinBase as BasePinSchema


def get_all_pins(db: Session) -> List[Pin]:
    return db.query(Pin)


def get_pin(db: Session, name: str) -> Pin:
    return db.query(Pin) \
        .filter(Pin.name == name) \
        .first()


def create_pin(db: Session, pin: BasePinSchema) -> Pin:
    point = WKTElement(
        f'POINT({pin.coordinates[0]} {pin.coordinates[1]})',
        srid=4326
    )
    db_item: Pin = Pin(
        name=pin.name,
        geom=point,
        map_id=pin.map_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item