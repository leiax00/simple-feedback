import json
from typing import Optional, List

from pydantic import BaseModel, Field, model_validator, field_validator, ConfigDict
from pydantic.alias_generators import to_camel

from server.entity.schema import Remark, BaseVO, Page, Author


class MessageBase(BaseVO):
    msg_id: Optional[int] = Field(default=None, description='消息ID')


class MessageQuery(Page):
    device_id: Optional[int] = Field(0, description='设备ID')
    owner_id: Optional[int] = Field(0, description='归属ID')

class Msg4TopicQuery(Page):
    topic_id: int = Field(description='主题ID')

class MessageCreate(Author, Remark):
    parent_id: Optional[int] = Field(default=0, description='父消息ID, 主题第一条为0')
    top_id: Optional[int] = Field(default=0, description='顶层消息ID, 主题第一条为0')
    device_id: int = Field(description='设备ID')
    owner_id: int = Field(description='归属ID')
    content: str = Field(description='内容')
    meta: dict = Field(default={}, description='元数据')

    @model_validator(mode="before")
    @classmethod
    def move_extra_fields_to_meta(cls, data):
        if not isinstance(data, dict):
            return data

        # 创建可修改的副本
        values = dict(data)

        # 获取模型定义的字段
        model_fields = cls.model_fields.keys()
        camel_fields = [to_camel(field) for field in model_fields]
        # 分离额外字段
        extra_fields = {
            k: v for k, v in values.items()
            if k not in model_fields and k not in camel_fields and k != 'meta'
        }

        # 合并 meta (新字段不覆盖原有 meta)
        meta = values.get('meta', {})
        values['meta'] = {**extra_fields, **meta}  # 原 meta 优先

        # 移除已处理的额外字段
        for key in extra_fields:
            del values[key]

        return values


class Message(MessageBase, Author, Remark):
    top_id: Optional[int] = Field(default=None, description='顶层消息ID')
    parent_id: Optional[int] = Field(default=None, description='父消息ID')
    owner_id: Optional[int] = Field(default=None, description='归属ID')
    device_id: Optional[int] = Field(default=None, description='设备ID')
    content: Optional[str] = Field(default=None, description='内容')
    meta: Optional[dict] = Field(default={}, description='元数据')

    @field_validator("meta", mode="before")
    @classmethod
    def convert_meta(cls, value):
        if isinstance(value, str):
            try:
                new_dict = json.loads(value)
                return { to_camel(k): v for k, v in new_dict.items()}  # 将字符串转换为字典
            except json.JSONDecodeError:
                return {"all": value}
        return value  # 不是字符串就直接返回

class MessageAll(BaseVO):
    info: Message
    subs: List[Message]