from pydantic import BaseModel
from typing import List
from geoalchemy2.shape import to_shape
from . import models


class PinBase(BaseModel):
    name: str
    coordinates: list

    map_id: int


class Pin(PinBase):
    id: int

    @classmethod
    def from_orm(cls, dbModel: models.Pin):
        geom = to_shape(dbModel.geom)

        return cls(
            id=dbModel.id,
            name=dbModel.name,
            coordinates=[geom.x, geom.y],
            map_id=dbModel.map_id
        )


class MapBase(BaseModel):
    name: str


class Map(MapBase):
    id: int
    pins: List[Pin]

    @classmethod
    def from_orm(cls, dbModel: models.Map):
        return cls(
            id=dbModel.id,
            name=dbModel.name,
            pins=[Pin.from_orm(dbPin) for dbPin in dbModel.pins]
        )
