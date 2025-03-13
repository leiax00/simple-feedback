from typing import List, Type

from sqlalchemy import and_
from sqlalchemy.orm import Session

from server.entity import schema, model


def validate_client(owner_id: int, device_id: int, db: Session):
    owner = get_owner_by_id(owner_id, db)
    device = get_device_by_id(device_id, db)
    relative = db.query(model.DeviceOwner).filter(and_(
        model.DeviceOwner.owner_id == owner_id,
        model.DeviceOwner.device_id == device_id
    )).first()
    if (not owner or not device or
            owner.status != '0' or device.status != '0' or
            not relative
    ):
        return False, None, None

    return True, owner, device


def get_valid_owner_list(db: Session) -> list[Type[model.DictData]]:
    query = db.query(model.DictData).filter(
        and_(model.DictData.dict_type == 'owner_type',
             model.DictData.status == '0')
    )
    return query.all()


def get_owner_list(db: Session) -> list[Type[model.Owner]]:
    query = db.query(model.Owner).filter(model.Owner.status == "0")
    return query.all()


def get_owner_by_code(code: str, db: Session) -> Type[model.Owner] | None:
    query = db.query(model.Owner).filter(and_(
        model.Owner.code == code
    ))
    return query.first()


def get_owner_by_id(owner_id: int, db: Session) -> Type[model.Owner] | None:
    query = db.query(model.Owner).filter(and_(
        model.Owner.owner_id == owner_id
    ))
    return query.first()


def get_device_by_key(device_key: str, db: Session) -> Type[model.Device] | None:
    query = db.query(model.Device).filter(model.Device.device_key == device_key)
    return query.first()


def get_device_by_id(device_id: int, db: Session) -> Type[model.Device] | None:
    query = db.query(model.Device).filter(model.Device.device_id == device_id)
    return query.first()


def get_device_list(q: schema.DeviceQuery, db: Session) -> tuple[int, List[Type[model.Device]]]:
    with db.begin():
        query = device_query(db, q)
        total = query.count()
        if q.page_size and q.page_num:
            query = query.limit(q.page_size).offset((q.page_num - 1) * q.page_size)
        device_list = query.all()
    return total, device_list


def device_query(db, q):
    query = db.query(model.Device)
    if q.device_id:
        query = query.filter(model.Device.device_id == q.device_id)
    if q.device_key:
        query = query.filter(model.Device.device_key == q.device_key)
    if q.code:
        query = query.join(model.DeviceOwner, model.DeviceOwner.device_id == model.Device.device_id).join(
            model.Owner, model.Owner.owner_id == model.DeviceOwner.owner_id).filter(model.Owner.code == q.code)
    return query
