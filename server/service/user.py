from sqlalchemy.orm import Session

from server.entity import model


def get_user_by_id(user_id: int, db: Session):
    return db.query(model.User).filter(model.User.user_id == user_id).first()


def get_user_by_username(username: str, db: Session):
    query = db.query(model.User).filter(model.User.username == username)
    return query.first()
