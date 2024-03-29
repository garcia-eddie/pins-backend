from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import schemas, crud


router = APIRouter(
    prefix="/maps",
    tags=["maps"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=schemas.Map)
def create_map(map: schemas.MapBase, db: Session = Depends(get_db)):
    rs = crud.create_map(db, map)
    response = schemas.Map.from_orm(rs)
    return response


@router.get("/", response_model=List[schemas.Map])
def get_maps(db: Session = Depends(get_db)):
    rs = crud.get_all_maps(db)
    response = [schemas.Map.from_orm(res) for res in rs]
    return response


@router.get("/{map_id}", response_model=schemas.Map)
def get_map(map_id: int, db: Session = Depends(get_db)):
    rs = crud.get_map(db, map_id)
    response = schemas.Map.from_orm(rs)
    return response
