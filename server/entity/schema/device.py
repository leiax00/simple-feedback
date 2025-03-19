from typing import Optional

from pydantic import BaseModel, Field

from server.entity.schema.baseVo import Remark, Page, Author, BaseVO


class DeviceBaseQuery(BaseVO):
    code: Optional[str] = Field(default=None, description='归属code')
    device_key: Optional[str] = Field(default=None, description='设备key')


class DeviceQuery(Page, DeviceBaseQuery):
    device_id: Optional[int] = Field(default=None, description='设备ID')


class DeviceVo(Author, Remark):
    device_id: Optional[int] = Field(default=None, description='设备ID')
    device_key: Optional[str] = Field(default=None, description='设备key')
    status: Optional[str] = Field(default=None, description='设备状态（0正常 1停用）')


class DeviceInitReply(BaseVO):
    device_id: Optional[int] = Field(default=None, description='设备ID')
    owner_id: Optional[int] = Field(default=None, description='归属者ID')
    access_token: Optional[str] = Field(default=None, description='分配的用户Bearer token, 有效期1小时')

class OwnerVo(Author, Remark):
    owner_id: int = Field(..., description='归属者ID')
    parent_id: int = Field(..., description='父归属者ID')
    owner_name: str = Field(..., description='归属者名称')
    order_num: int = Field(..., description='显示顺序')
    code: str = Field(..., description='归属code')
    visible: str = Field(..., description='是否可见')
    status: str = Field(..., description='状态（0正常 1停用）')
    icon: str = Field(..., description='图标')