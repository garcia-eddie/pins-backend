from sqlalchemy.orm import Session
from . import models, schemas
from geoalchemy2 import WKTElement
from typing import List


def get_map(db: Session, id: int) -> models.Map:
    return db.query(models.Map) \
        .filter(models.Map.id == id) \
        .first()


def get_all_maps(db: Session) -> List[models.Map]:
    return db.query(models.Map)


def get_all_pins(db: Session) -> List[models.Pin]:
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
    db_item: models.Pin = models.Pin(
        name=pin.name,
        geom=point,
        map_id=pin.map_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_map(db: Session, map: schemas.MapBase) -> models.Map:
    db_item: models.Map = models.Map(name=map.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
