from fastapi import FastAPI
from . import models
from .routers import maps, pins
from .database.database import engine

app = FastAPI()
app.include_router(maps.router)
app.include_router(pins.router)

models.Base.metadata.create_all(bind=engine)
