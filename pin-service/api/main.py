from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Annotated
from api.routers.maps import router as mapRouter
from api.routers.pins import router as pinRouter

app = FastAPI()
app.include_router(mapRouter)
app.include_router(pinRouter)

fake_users_db = {
    "eddie": {
        "username": "eddie",
        "hashed_password": "HASH12345",
        "disabled": False
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def hash_password(password: str) -> str:
    return "HASH" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid Authentication Credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user


def get_current_active_user(currentUser: Annotated[User, Depends(get_current_user)]):
    if currentUser.disabled:
        raise HTTPException(
            status_code=400, detail="User Not Found or Disabled")
    return currentUser


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_data = fake_users_db.get(form_data.username)
    if not user_data:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    user = UserInDB(**user_data)
    hashed_password = hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/me")
def get_me(currentUser: Annotated[User, Depends(get_current_active_user)]):
    return currentUser
