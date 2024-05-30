from sqlalchemy.orm import Session

from api.database.models import User
from api.schemas.schema_user import CreateUserRequest


def get_user(db: Session, username: str) -> User:
    return db.query(User) \
        .filter(User.username == username) \
        .first()


def create_user(db: Session, user: CreateUserRequest) -> User:
    db_item: User = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
