from fastapi import Depends, FastAPI
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


@app.get("/pins")
def get_pins(db: Session = Depends(get_db)):
    rs = crud.get_all(db)
    response = [schemas.RLocation.from_orm(res) for res in rs]
    return response


@app.put("/coords")
def create_coords(location: schemas.Location):
    print(location)
    return {"Hello": "World"}


@app.post("/", response_model=schemas.RLocation)
def create_restaurant_location(rLocationBase: schemas.RLocationBase, db: Session = Depends(get_db)):
    rs = crud.create_restaurant_location(db, rLocationBase)
    response = schemas.RLocation.from_orm(rs)
    return response
