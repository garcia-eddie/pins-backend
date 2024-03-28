from fastapi import Depends, FastAPI
from typing import List
from sqlalchemy.orm import Session


from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/maps", response_model=schemas.Map)
def create_map(map: schemas.MapBase, db: Session = Depends(get_db)):
    rs = crud.create_map(db, map)
    response = schemas.Map.from_orm(rs)
    return response


@app.get("/maps/{map_id}", response_model=schemas.Map)
def get_map(map_id: int, db: Session = Depends(get_db)):
    rs = crud.get_map(db, map_id)
    response = schemas.Map.from_orm(rs)
    return response


@app.get("/maps", response_model=List[schemas.Map])
def get_maps(db: Session = Depends(get_db)):
    rs = crud.get_all_maps(db)
    response = [schemas.Map.from_orm(res) for res in rs]
    return response


@app.post("/pins", response_model=schemas.Pin)
def create_pin(pin: schemas.PinBase, db: Session = Depends(get_db)):
    rs = crud.create_pin(db, pin)
    response = schemas.Pin.from_orm(rs)
    return response


@app.get("/pins", response_model=List[schemas.Pin])
def get_pins(db: Session = Depends(get_db)):
    rs = crud.get_all_pins(db)
    response = [schemas.Pin.from_orm(res) for res in rs]
    return response
