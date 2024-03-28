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
    response = [schemas.Pin.from_orm(res) for res in rs]
    return response


@app.post("/", response_model=schemas.Pin)
def create_pin(pin: schemas.PinBase, db: Session = Depends(get_db)):
    rs = crud.create_pin(db, pin)
    response = schemas.Pin.from_orm(rs)
    return response
