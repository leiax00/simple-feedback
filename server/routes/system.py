from datetime import timedelta
from typing import Annotated

from fastapi import status, APIRouter, Depends, HTTPException, Request, Form
from fastapi_login import LoginManager
from sqlalchemy.orm import Session

from server import service
from server.context import database
from server.context.security import manager
from server.entity import schema
from server.entity.schema import R, UserLogin
from server.utils.bcrypt_util import verify_password

router = APIRouter(prefix='/system/v1', tags=['System'])


@router.post(
    "/init",
    response_model=R[schema.DeviceInitReply],
    response_model_exclude_none=True
)
async def start_feedback(
        request: schema.DeviceBaseQuery,
        db: Session = Depends(database.session)
):
    owner, device = service.init(request, db)
    if not device or not owner:
        return R(code=status.HTTP_403_FORBIDDEN, msg="invalid_device")

    token = manager.create_access_token(
        data={"sub": f"user_{request.device_key}"},
        expires=timedelta(hours=1)
    )
    return R(data=schema.DeviceInitReply(
        device_id=device.device_id,
        owner_id=owner.owner_id,
        access_token=token,
    ))





@router.post(
    "/login",
)
async def login(
        request: Request,
        db: Session = Depends(database.session)):
    content_type = request.headers.get("content-type")

    if "application/json" in content_type:
        login_info = UserLogin.model_validate(await request.json())
    elif "application/x-www-form-urlencoded" in content_type:
        login_info = UserLogin.model_validate(await request.form())
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = service.user.get_user_by_username(login_info.username, db)
    if not user or not verify_password(login_info.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = manager.create_access_token(data={"sub": user.username})
    return { "access_token": token, "token_type": "bearer" }
