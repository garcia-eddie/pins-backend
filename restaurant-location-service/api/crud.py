from sqlalchemy.orm import Session
from . import models, schemas
from geoalchemy2 import WKTElement
from typing import List


def get_all(db: Session) -> List[models.RLocationModel]:
    return db.query(models.RLocationModel)


def get_restaurant_location(db: Session, name: str) -> models.RLocationModel:
    return db.query(models.RLocationModel) \
        .filter(models.RLocationModel.name == name) \
        .first()


def create_restaurant_location(db: Session, rLocation: schemas.RLocationBase) -> models.RLocationModel:
    point = WKTElement(
        f'POINT({rLocation.coordinates[0]} {rLocation.coordinates[1]})',
        srid=4326
    )
    db_item = models.RLocationModel(name=rLocation.name, geom=point)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
