# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class BaseVO(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )

class Author(BaseVO):
    create_time: datetime = Field(default=datetime.now(), description='创建时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    update_by: Optional[str] = Field(default=None, description='更新者')


class Remark(BaseVO):
    remark: Optional[str] = Field(default=None, description='备注信息')


class Page(BaseVO):
    page_num: Optional[int] = Field(default=1, description='页码')
    page_size: Optional[int] = Field(default=10, description='每页数量')


class Order(BaseVO):
    order_by: Optional[str] = Field(default=None, description='排序字段')
    order: Optional[str] = Field(default="desc", description='排序方式')
