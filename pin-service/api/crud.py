from sqlalchemy.orm import Session
from . import models, schemas
from geoalchemy2 import WKTElement
from typing import List


def get_all(db: Session) -> List[models.PinModel]:
    return db.query(models.PinModel)


def get_pin(db: Session, name: str) -> models.PinModel:
    return db.query(models.PinModel) \
        .filter(models.PinModel.name == name) \
        .first()


def create_pin(db: Session, pin: schemas.PinBase) -> models.PinModel:
    point = WKTElement(
        f'POINT({pin.coordinates[0]} {pin.coordinates[1]})',
        srid=4326
    )
    db_item = models.PinModel(name=pin.name, geom=point)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
