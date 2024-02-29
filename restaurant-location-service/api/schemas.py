from pydantic import BaseModel
from typing import List
from geoalchemy2.shape import to_shape
from .models import RLocationModel


class Location(BaseModel):
    coordinates: List[float]


class RLocationBase(BaseModel):
    name: str
    coordinates: list


class RLocation(RLocationBase):
    id: int

    @classmethod
    def from_orm(cls, dbModel: RLocationModel):
        geom = to_shape(dbModel.geom)

        print(dbModel.id)
        print(dbModel.name)
        print(geom.x)
        print(geom.y)
        return cls(
            id=dbModel.id,
            name=dbModel.name,
            coordinates=[geom.x, geom.y]
        )

    # def to_orm(self) -> RestaurantLocationModel:
    #     point = Point(self.coordinates).wkb_hex()
    #     return RestaurantLocationModel(name=self.name, geom=point)
