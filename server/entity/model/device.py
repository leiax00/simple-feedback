from sqlalchemy import Column, BigInteger, String, DateTime, CHAR, text
from server.context.database import Base

class Device(Base):
    __tablename__ = "fb_device"

    device_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='设备ID')
    device_key = Column(String(200), server_default='', comment='设备key')
    status = Column(CHAR(1), server_default='0', comment='设备状态（0正常 1停用）')
    create_by = Column(String(64), server_default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(64), server_default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间')
    remark = Column(String(500), server_default='', comment='备注')

from sqlalchemy import Column, BigInteger, Integer, String, CHAR, DateTime
from server.context.database import Base

class Owner(Base):
    __tablename__ = "fb_owner"

    owner_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='归属者ID')
    owner_name = Column(String(50), nullable=False, comment='归属者名称')
    parent_id = Column(BigInteger, server_default=text('0'), comment='父归属者ID')
    order_num = Column(Integer, server_default=text('0'), comment='显示顺序')
    code = Column(String(200), server_default='', comment='归属者代码')
    visible = Column(CHAR(1), server_default='0', comment='归属者可视状态（0显示 1隐藏）')
    status = Column(CHAR(1), server_default='0', comment='归属者状态（0正常 1停用）')
    icon = Column(String(100), server_default='#', comment='归属者图标')
    create_by = Column(String(64), server_default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(64), server_default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间')
    remark = Column(String(500), server_default='', comment='备注')

from sqlalchemy import Column, BigInteger
from server.context.database import Base

class DeviceOwner(Base):
    __tablename__ = "fb_device_owner"

    device_id = Column(BigInteger, primary_key=True, comment='设备ID')
    owner_id = Column(BigInteger, primary_key=True, comment='归属者ID')