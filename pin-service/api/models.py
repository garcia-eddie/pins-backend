from sqlalchemy import Column, String, Integer
from .database import Base
from geoalchemy2 import Geometry


class PinModel(Base):
    __tablename__ = "pin"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
