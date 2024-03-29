from pydantic import BaseModel
from typing import List
from .schema_pin import PinResponse
from ..database.models import Map


class MapBase(BaseModel):
    name: str


class CreateMapRequest(MapBase):
    pass


class MapResponse(MapBase):
    id: int
    pins: List[PinResponse]

    @classmethod
    def from_orm(cls, dbModel: Map):
        return cls(
            id=dbModel.id,
            name=dbModel.name,
            pins=[PinResponse.from_orm(dbPin) for dbPin in dbModel.pins]
        )
