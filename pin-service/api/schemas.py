from pydantic import BaseModel
from geoalchemy2.shape import to_shape
from .models import PinModel


class PinBase(BaseModel):
    name: str
    coordinates: list


class Pin(PinBase):
    id: int

    @classmethod
    def from_orm(cls, dbModel: PinModel):
        geom = to_shape(dbModel.geom)

        return cls(
            id=dbModel.id,
            name=dbModel.name,
            coordinates=[geom.x, geom.y]
        )
