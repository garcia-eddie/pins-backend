from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from api.routers.maps import router as mapRouter
from api.routers.pins import router as pinRouter
from api.database import db_user
from api.database.database import get_db
from api.database.models import User
from api.schemas.schema_user import CreateUserRequest, UserBase

app = FastAPI()
app.include_router(mapRouter)
app.include_router(pinRouter)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    return "HASH" + password


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token):
#     user = get_user(fake_users_db, token)
#     return user


# def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=400,
#             detail="Invalid Authentication Credentials",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     return user


# def get_current_active_user(currentUser: Annotated[User, Depends(get_current_user)]):
#     if currentUser.disabled:
#         raise HTTPException(
#             status_code=400, detail="User Not Found or Disabled")
#     return currentUser


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    rs = db_user.create_user(db, user)
    if not rs:
        raise HTTPException(status_code=404, detail="User Not Created")

    return {"detail": "User created, please log in"}


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user_data: User = db_user.get_active_user(db, form_data.username)
    if not user_data:
        raise HTTPException(
            status_code=400, detail="Incorrect username")

    user = UserBase.from_orm(user_data)
    hashed_password = hash_password(form_data.password)
    if hashed_password != user.hashed_password:
        raise HTTPException(
            status_code=404, detail="Incorrect password")

    return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/me")
# def get_me(currentUser: Annotated[User, Depends(get_current_active_user)]):
#     return currentUser
