from typing import List, Annotated

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from starlette import status

from server import service
from server.context import database
from server.context.security import manager
from server.entity import schema
from server.entity.schema import R, PageR

router = APIRouter(prefix='/message/v1', tags=['Message'])


@router.get(
    "/list/topic",
    response_model=PageR[list[schema.Message]],
    response_model_exclude_none=True,
    description='获取问题反馈主题列表(每个问题的第一条消息)'
)
async def get_topic_list(
        q: Annotated[schema.MessageQuery, Query()],
        db: Session = Depends(database.session),
        user: str = Depends(manager)
):
    """
    获取问题反馈列表
    """
    with db.begin():
        total, topic_list = service.message.topic_list(q, db)
    return PageR(rows=topic_list, total=total)

@router.get(
    "/list/topic-all",
    response_model=PageR[list[schema.MessageAll]],
    response_model_exclude_none=True,
    description='获取问题反馈列表, 包括子消息'
)
async def topic_all_in_one(
        q: Annotated[schema.MessageQuery, Query()],
        db: Session = Depends(database.session),
        user: str = Depends(manager)
):
    """
    获取问题反馈列表, 包括子消息
    """
    total, topic_list = service.message.topic_all_in_one(q, db)
    return PageR(rows=topic_list, total=total)

@router.get(
    "/topic/all",
    response_model=PageR[list[schema.Message]],
    response_model_exclude_none=True,
    description='获取一个主题下所有消息'
)
async def message_list_4_topic(
    q: Annotated[schema.Msg4TopicQuery, Query()],
    db: Session = Depends(database.session),
    user: str = Depends(manager)
):
    """
    获取一个主题下所有消息
    """
    total, msg_list = service.message.message_list_4_topic(q, db)
    return PageR(rows=msg_list, total=total)


@router.post(
    "/new",
    response_model=R[schema.MessageBase],
    response_model_exclude_none=True,
    summary='添加问题反馈',
    description="""
1. 新增需要的字段, meta字段可以自定义, 目前想到的是记录手机型号, APP版本, 设备版本等信息
```json
{
  "deviceId": 0,
  "ownerId": 0,
  "content": "string",
  "meta": {}
}
```
2. 回复消息需要的字段
```json
{
  "topId": 0,
  "parentId": 0,
  "ownerId": 0,
  "deviceId": 0,
  "content": "string",
  "meta": {}
}
```
"""
)
async def new_message(
        msg: schema.MessageCreate,
        db: Session = Depends(database.session),
        user: str = Depends(manager)
):
    """
    添加问题反馈
    :param user: 用户名
    :param msg: 反馈内容
    :param db: 数据库连接
    """
    msg.create_by = user
    message = service.message.new_message(msg, db)
    if not message:
        return R(code=status.HTTP_400_BAD_REQUEST, msg='添加失败')
    return R(data=message)
