from sqlalchemy import Column, BigInteger, Integer, String, CHAR, DateTime, text
from server.context.database import Base

class DictData(Base):
    __tablename__ = "fb_dict_data"

    dict_code = Column(BigInteger, primary_key=True, autoincrement=True, comment='字典编码')
    dict_sort = Column(Integer, server_default=text('0'), comment='字典排序')
    dict_label = Column(String(100), server_default='', comment='字典标签/I18n键')
    dict_value = Column(String(100), server_default='', comment='字典键值')
    dict_type = Column(String(100), server_default='', comment='字典类型')
    is_default = Column(CHAR(1), server_default='N', comment='是否默认（Y是 N否）')
    status = Column(CHAR(1), server_default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), server_default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(64), server_default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间')
    remark = Column(String(500), comment='备注')

class DictType(Base):
    __tablename__ = "fb_dict_type"

    dict_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='字典主键')
    dict_name = Column(String(100), server_default='', comment='字典名称')
    dict_type = Column(String(100), server_default='', unique=True, comment='字典类型')
    status = Column(CHAR(1), server_default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), server_default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(64), server_default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间')
    remark = Column(String(500), comment='备注')