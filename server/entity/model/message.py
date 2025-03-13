from sqlalchemy import Column, BigInteger, Text, String, DateTime, text
from server.context.database import Base

class Message(Base):
    __tablename__ = "fb_message"

    msg_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='消息ID')
    top_id = Column(BigInteger, server_default=text('0'), comment='顶层消息ID')
    parent_id = Column(BigInteger, server_default=text('0'), comment='父消息ID')
    owner_id = Column(BigInteger, nullable=False, comment='归属ID')
    device_id = Column(BigInteger, nullable=False, comment='设备ID')
    content = Column(Text, server_default='', comment='内容')
    meta = Column(Text, server_default='', comment='元数据, json字符串')
    create_by = Column(String(64), server_default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(64), server_default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间')
    remark = Column(String(500), server_default='', comment='备注')