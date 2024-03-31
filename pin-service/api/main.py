from fastapi import FastAPI
from .routers import maps, pins

app = FastAPI()
app.include_router(maps.router)
app.include_router(pins.router)
