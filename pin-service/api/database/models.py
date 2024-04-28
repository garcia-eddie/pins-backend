from geoalchemy2 import Geometry
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from typing import List


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String)
    disabled: Mapped[bool] = mapped_column(default=False)

    maps: Mapped[List["Map"]] = relationship(back_populates="user")


class Map(Base):
    __tablename__ = "map"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="maps")
    pins: Mapped[List["Pin"]] = relationship(back_populates="map")


class Pin(Base):
    __tablename__ = "pin"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    geom: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type='POINT', srid=4326))
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))

    map: Mapped["Map"] = relationship(back_populates="pins")
