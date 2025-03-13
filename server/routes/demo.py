from typing import Annotated

from fastapi import FastAPI, APIRouter, Query
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

router = APIRouter(prefix='/demo/v1', tags=['Demo'])

# 请求模型
class CreateUserRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    user_id: int
    user_name: str

# 响应模型
class UserResponse(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

    user_id: int
    user_name: str

@router.post("/users", response_model=UserResponse)
async def create_user(user: CreateUserRequest):
    # 内部使用下划线字段名
    print(f"创建用户: {user.user_id} - {user.user_name}")
    return user

@router.get("/user/get", response_model=UserResponse)
async def create_user(user: Annotated[CreateUserRequest, Query()]):
    # 内部使用下划线字段名
    print(f"创建用户: {user.user_id} - {user.user_name}")
    return user

# 测试请求
# curl -X POST http://localhost:8000/users \
# -H "Content-Type: application/json" \
# -d '{"userId":123,"userName":"Alice"}'
