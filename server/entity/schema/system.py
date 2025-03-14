from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from server.entity.schema import Author, Remark, BaseVO


class UserBase(Author, Remark):
    user_id: Optional[int] = Field(None, description="用户ID")
    username: str = Field(..., max_length=30, description="用户账号")
    nickname: Optional[str] = Field("", max_length=30, description="用户昵称")
    user_type: Optional[str] = Field("00", max_length=2, description="用户类型（00系统用户）")
    email: Optional[str] = Field("", max_length=50, description="用户邮箱")
    phone_number: Optional[str] = Field("", max_length=11, description="手机号码")
    sex: Optional[str] = Field("0", max_length=1, description="用户性别（0男 1女 2未知）")
    avatar: Optional[str] = Field("", max_length=100, description="头像地址")
    password: Optional[str] = Field("", max_length=100, description="密码")
    status: Optional[str] = Field("0", max_length=1, description="帐号状态（0正常 1停用）")
    del_flag: Optional[str] = Field("0", max_length=1, description="删除标志（0代表存在 2代表删除）")
    login_ip: Optional[str] = Field("", max_length=128, description="最后登录IP")
    login_date: Optional[datetime] = Field(None, description="最后登录时间")
    create_by: Optional[str] = Field("", max_length=64, description="创建者")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_by: Optional[str] = Field("", max_length=64, description="更新者")
    update_time: Optional[datetime] = Field(None, description="更新时间")
    remark: Optional[str] = Field(None, max_length=500, description="备注")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "test_user",
                "nickname": "测试用户",
                "password": "secure_password"
            }
        }

class UserLogin(BaseVO):
    username: str = Field(None, max_length=30, description="用户账号")
    password: str = Field(None, max_length=100, description="密码")


class UserCreate(UserBase):
    password: str = Field(..., max_length=100, description="密码")

class UserResponse(UserBase):
    user_id: int = Field(..., description="用户ID")
    password: Optional[str] = Field(None, exclude=True)  # 排除密码字段