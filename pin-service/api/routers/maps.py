from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from api.database import db_map
from api.database.database import get_db
from api.schemas.schema_map import CreateMapRequest, MapResponse


router = APIRouter(
    prefix="/maps",
    tags=["maps"],
    dependencies=[Depends(get_db)]
)


@router.post("/", response_model=MapResponse)
def create_map(map: CreateMapRequest, db: Session = Depends(get_db)):
    rs = db_map.create_map(db, map)
    if not rs:
        raise HTTPException(status_code=404, detail="Map Not Created")
    response = MapResponse.from_orm(rs)
    return response


@router.get("/{map_id}", response_model=MapResponse)
def get_map(map_id: int, db: Session = Depends(get_db)):
    rs = db_map.get_map(db, map_id)
    if not rs:
        raise HTTPException(status_code=404, detail="Map Not Found")
    response = MapResponse.from_orm(rs)
    return response


@router.get("/", response_model=List[MapResponse])
def get_maps(db: Session = Depends(get_db)):
    rs = db_map.get_all_maps(db)
    if not rs:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    response = [MapResponse.from_orm(res) for res in rs]
    return response
