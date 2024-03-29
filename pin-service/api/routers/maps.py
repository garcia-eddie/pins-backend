from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import db_map
from ..database.database import get_db
from ..schemas.schema_map import CreateMapRequest, MapResponse


router = APIRouter(
    prefix="/maps",
    tags=["maps"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=MapResponse)
def create_map(map: CreateMapRequest, db: Session = Depends(get_db)):
    rs = db_map.create_map(db, map)
    response = MapResponse.from_orm(rs)
    return response


@router.get("/{map_id}", response_model=MapResponse)
def get_map(map_id: int, db: Session = Depends(get_db)):
    rs = db_map.get_map(db, map_id)
    response = MapResponse.from_orm(rs)
    return response


@router.get("/", response_model=List[MapResponse])
def get_maps(db: Session = Depends(get_db)):
    rs = db_map.get_all_maps(db)
    response = [MapResponse.from_orm(res) for res in rs]
    return response
