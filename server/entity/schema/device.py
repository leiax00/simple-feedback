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
