from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base
from geoalchemy2 import Geometry


class Pin(Base):
    __tablename__ = "pin"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    geom: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326))
