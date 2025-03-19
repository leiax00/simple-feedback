import json

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from server.entity import schema, model
from .device import validate_client


def new_message(msg: schema.MessageCreate, db: Session):
    with db.begin():
        ok, owner, device = validate_client(msg.owner_id, msg.device_id, db)
        if not ok:
            return None

        msg_model = model.Message(
            top_id=msg.top_id,
            parent_id=msg.parent_id,
            device_id=msg.device_id,
            owner_id=msg.owner_id,
            content=msg.content,
            meta=json.dumps(msg.meta),
            create_by=msg.create_by or "client",
            create_time=msg.create_time,
            remark=msg.remark,
        )
        db.add(msg_model)
        db.query(model.Message).filter_by(
            top_id=msg.top_id
        ).update(
            {model.Message.update_time: msg.create_time}
        )
        db.commit()
    db.refresh(msg_model)
    return msg_model


def topic_all_in_one(q: schema.MessageQuery, db):
    msg_all = []
    with db.begin():
        total, topics = topic_list(q, db)
        for topic in topics:
            total, msgs = message_list_4_topic(schema.Msg4TopicQuery(
                topic_id=topic.msg_id,
                page_size=0,
                page_num=0
            ), db)
            msg_all.append(schema.MessageAll(
                info=schema.Message(**topic.__dict__),
                subs=[schema.Message(**msg.__dict__) for msg in msgs]
            ))
    return total, msg_all


def topic_list(q: schema.MessageQuery, db):
    query = db.query(model.Message).filter(and_(
        model.Message.top_id == 0,
        model.Message.parent_id == 0
    ))
    if q.owner_id > 0:
        query = query.filter(model.Message.owner_id == q.owner_id)
    if q.device_id > 0:
        query = query.filter(model.Message.device_id == q.device_id)
    total = query.count()
    query = query.order_by(model.Message.update_time.desc())
    if q.page_size and q.page_num:
        query = query.limit(q.page_size).offset((q.page_num - 1) * q.page_size)
    topics = query.all()
    return total, topics


def message_list_4_topic(q: schema.Msg4TopicQuery, db):
    query = db.query(model.Message).filter(
        or_(model.Message.top_id == q.topic_id, model.Message.msg_id == q.topic_id)).order_by(
        model.Message.top_id.asc(),
        model.Message.parent_id.asc(),
    )
    total = query.count()
    if q.page_size and q.page_num:
        query = query.limit(q.page_size).offset((q.page_num - 1) * q.page_size)
    return total, query.all()
