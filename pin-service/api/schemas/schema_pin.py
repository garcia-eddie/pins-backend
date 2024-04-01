from pydantic import BaseModel
from geoalchemy2.shape import to_shape

from api.database.models import Pin


class PinBase(BaseModel):
    name: str
    coordinates: list

    map_id: int


class CreatePinRequest(PinBase):
    pass


class PinResponse(PinBase):
    id: int

    @classmethod
    def from_orm(cls, dbModel: Pin):
        geom = to_shape(dbModel.geom)

        return cls(
            id=dbModel.id,
            name=dbModel.name,
            coordinates=[geom.x, geom.y],
            map_id=dbModel.map_id
        )
