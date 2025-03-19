from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from server.entity import model, schema
from server.utils.bcrypt_util import hash_password


def get_user_by_id(user_id: int, db: Session):
    return db.query(model.User).filter(model.User.user_id == user_id).first()


def get_user_by_username(username: str, db: Session):
    query = db.query(model.User).filter(model.User.username == username)
    return query.first()

def add_user(user: schema.UserCreate, db: Session):
    try:
        user_model = model.User(
            username=user.username,
            password=hash_password(user.password),
            nickname=user.nickname,
            email=user.email,
            user_type=user.user_type,
            phone_number=user.phone_number,
            sex=user.sex,
            avatar=user.avatar,
            status=user.status,
            del_flag=user.del_flag,
            remark=user.remark,
            create_time=user.create_time,
            create_by=user.create_by,
        )
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
        return user_model
    except IntegrityError as e:
        db.rollback()  # 回滚事务
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists."
        )