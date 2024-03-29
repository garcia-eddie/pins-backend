from fastapi import FastAPI

from . import models
from .database import engine
from .routers import maps, pins

app = FastAPI()
app.include_router(maps.router)
app.include_router(pins.router)

models.Base.metadata.create_all(bind=engine)
