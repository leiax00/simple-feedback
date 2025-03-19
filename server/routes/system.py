from datetime import timedelta
from typing import Annotated, Optional, Dict

from fastapi import status, APIRouter, Depends, HTTPException, Request, Form, Body
from fastapi_login import LoginManager
from sqlalchemy.orm import Session

from server import service
from server.context import database
from server.context.security import manager
from server.entity import schema
from server.entity.schema import R
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


async def parse_login_info(request: Request):
    content_type = request.headers.get("content-type")
    if "application/json" in content_type:
        # 解析 JSON 数据
        json_data = await request.json()
        return schema.UserLogin(**json_data)
    elif "application/x-www-form-urlencoded" in content_type:
        # 解析表单数据
        form_data = await request.form()
        return schema.UserLogin(username=form_data.get("username"), password=form_data.get("password"))
    else:
        raise HTTPException(status_code=400, detail="Invalid content type")


@router.post(
    "/login",
    response_model=Dict[str, str],
    summary="用户登录",
    description="支持表单提交和 JSON 提交, 参数为 username 和 password",
    response_description="返回 access_token 和 token_type"
)
async def login(
        login_info: schema.UserLogin = Depends(parse_login_info),
        db: Session = Depends(database.session)):
    user = service.user.get_user_by_username(login_info.username, db)
    if not user or not verify_password(login_info.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = manager.create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get(
    "/user/info",
    response_model=R[schema.User],
    response_model_exclude_none=True
)
async def get_user_info(
        username: str = Depends(manager),
        db: Session = Depends(database.session)
):
    user = service.user.get_user_by_username(username, db)
    return R(data=user)


@router.post(
    "/user/register",
    response_model=R[schema.User],
    response_model_exclude_none=True
)
async def register_user(
        user_info: schema.UserCreate,
        username: str = Depends(manager),
        db: Session = Depends(database.session)
):
    user_info.create_by = username
    user = service.user.add_user(user_info, db)
    return R(data=user)
