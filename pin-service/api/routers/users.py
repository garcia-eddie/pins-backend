from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Annotated

from api.database import db_user
from api.database.database import get_db
from api.database.models import User
from api.schemas.schema_user import CreateUserRequest
from api.schemas.schema_token import Token, TokenData

import jwt
from jwt.exceptions import InvalidTokenError

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

SECRET_KEY = '5dab3778e71440759d4d7a0ede85dff979320250a5bf7baa631d20f12a64a02b'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def create_access_token(
    data: dict,
    expires_delta: timedelta | None = None
) -> str:
    """
    Parameters:
    data (dict): The data to be encoded.

    expires_delta (timedelta):  The time difference between two
        datetime objects.

    Returns:
    str : an encoded jwt.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, db: Session):
    user = db_user.get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password
    rs = db_user.create_user(db, user)
    if not rs:
        raise HTTPException(status_code=404, detail="User Not Created")

    return {"detail": "User created, please log in"}


@router.post("/token")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    user_data: User = authenticate_user(
        form_data.username,
        form_data.password,
        db
    )
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_data.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    user = db_user.get_user(db, token_data.username)
    if not user:
        raise credentials_exception
    return user


def get_current_active_user(
    currentUser: Annotated[
        User,
        Depends(get_current_user)
    ]
):
    if currentUser.disabled:
        raise HTTPException(
            status_code=400,
            detail="User not found or disabled"
        )
    return currentUser


@ router.get("/me")
def get_me(currentUser: Annotated[User, Depends(get_current_active_user)]):
    return currentUser
