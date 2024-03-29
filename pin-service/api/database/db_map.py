from sqlalchemy.orm import Session
from typing import List
from .models import Map
from .. import schemas


def get_map(db: Session, id: int) -> Map:
    return db.query(Map) \
        .filter(Map.id == id) \
        .first()


def get_all_maps(db: Session) -> List[Map]:
    return db.query(Map)


def create_map(db: Session, map: schemas.MapBase) -> Map:
    db_item: Map = Map(name=map.name)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
