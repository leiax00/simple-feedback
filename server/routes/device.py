from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from starlette import status

from server import service
from server.context import database
from server.context.security import manager
from server.entity import schema, model
from server.entity.schema import PageR, R

router = APIRouter(prefix='/device/v1', tags=['Device'])

@router.get(
    "/list",
    response_model=PageR[list[schema.DeviceVo]],
    response_model_exclude_none=True
)
async def get_device_list(
        q: Annotated[schema.DeviceQuery, Query()],
        db: Session = Depends(database.session),
        user: str = Depends(manager)
):
    print(user)
    total, device_list = service.get_device_list(q, db)
    return PageR(rows=device_list, total=total)

@router.get(
    "/get/{device_id}",
    response_model=R[schema.DeviceVo],
    response_model_exclude_none=True
)
async def get_device_by_id(
        device_id: int,
        db: Session = Depends(database.session),
        user: str = Depends(manager)
):
    device = service.get_device_by_id(device_id, db)
    if not device:
        return R(code=status.HTTP_404_NOT_FOUND, msg="not_found")
    return R(data=device)

@router.get(
    "/key/{device_key}",
    response_model=R[schema.DeviceVo],
    response_model_exclude_none=True
)
async def get_device_by_key(
        device_key: str,
        db: Session = Depends(database.session),
        user: str = Depends(manager)
):
    device = service.get_device_by_key(device_key, db)
    if not device:
        return R(code=status.HTTP_404_NOT_FOUND, msg="not_found")
    return R(data=device)