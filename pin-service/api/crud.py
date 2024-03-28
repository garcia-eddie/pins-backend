from sqlalchemy.orm import Session
from . import models, schemas
from geoalchemy2 import WKTElement
from typing import List


def get_all(db: Session) -> List[models.Pin]:
    return db.query(models.Pin)


def get_pin(db: Session, name: str) -> models.Pin:
    return db.query(models.Pin) \
        .filter(models.Pin.name == name) \
        .first()


def create_pin(db: Session, pin: schemas.PinBase) -> models.Pin:
    point = WKTElement(
        f'POINT({pin.coordinates[0]} {pin.coordinates[1]})',
        srid=4326
    )
    db_item = models.Pin(name=pin.name, geom=point)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
