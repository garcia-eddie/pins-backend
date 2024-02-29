from sqlalchemy import Column, String, Integer
from .database import Base
from geoalchemy2 import Geometry


class RLocationModel(Base):
    __tablename__ = "restaurant_location"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='POINT', srid=4326))
