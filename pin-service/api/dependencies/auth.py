from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,
import jwt

SECRET_KEY = '5dab3778e71440759d4d7a0ede85dff979320250a5bf7baa631d20f12a64a02b'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(
    db: Session,
    username: str,
    password: str
):
    user = db_user.get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None

        token_data = TokenData(username=username)

    except InvalidTokenError:
        return None

    user = db_user.get_user(db, token_data.username)
    if not user:
        raise credentials_exception
    return user


def create_access_token(
    data: dict
) -> str:
    """
    Parameters:
    data (dict): The data to be encoded.

    expires_delta (timedelta):  The time difference between two
        datetime objects.

    Returns:
    str : an encoded jwt.
    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
