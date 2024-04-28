from pydantic import BaseModel

from api.database.models import User


class UserBase(BaseModel):
    username: str
    hashed_password: str

    @classmethod
    def from_orm(cls, dbModel: User):
        return cls(
            username=dbModel.username,
            hashed_password=dbModel.hashed_password
        )


class UserResponse(UserBase):
    id: int
    email: str | None = None
    disabled: bool | None = None

    @classmethod
    def from_orm(cls, dbModel: User):
        return cls(
            id=dbModel.id,
            username=dbModel.username,
            hashed_password=dbModel.hashed_password,
            email=dbModel.email,
            disabled=dbModel.disabled
        )


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str
