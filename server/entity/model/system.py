from sqlalchemy import Column, BigInteger, String, CHAR, DateTime, text

from server.context.database import Base


class User(Base):
    __tablename__ = "fb_user"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, comment='用户ID')
    username = Column(String(30), name="user_name", nullable=False, comment='用户账号')
    nickname = Column(String(30), name="nick_name", nullable=False, comment='用户昵称')
    user_type = Column(String(2), server_default='00', comment='用户类型（00系统用户）')
    email = Column(String(50), server_default='', comment='用户邮箱')
    phone_number = Column(String(11), server_default='', comment='手机号码')
    sex = Column(CHAR(1), server_default='0', comment='用户性别（0男 1女 2未知）')
    avatar = Column(String(100), server_default='', comment='头像地址')
    password = Column(String(100), server_default='', comment='密码')
    status = Column(CHAR(1), server_default='0', comment='帐号状态（0正常 1停用）')
    del_flag = Column(CHAR(1), server_default='0', comment='删除标志（0代表存在 2代表删除）')
    login_ip = Column(String(128), server_default='', comment='最后登录IP')
    login_date = Column(DateTime, comment='最后登录时间')
    create_by = Column(String(64), server_default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间')
    update_by = Column(String(64), server_default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间')
    remark = Column(String(500), comment='备注')
