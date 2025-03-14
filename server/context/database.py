from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

from server.context.config import config

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{config.db_config.username}:{config.db_config.password}@{config.db_config.host}:{config.db_config.port}/{config.db_config.database}?charset=utf8"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,  # 打印sql日志
    # poolclass=QueuePool,  # 显式指定连接池类型, 默认QueuePool
    pool_size=4,         # 常规保持10个连接, CPU核心数 × 2
    max_overflow=8,      # 允许临时增加连接, pool_size × 2
    pool_recycle=1800,    # 30分钟回收连接（小于MySQL的wait_timeout）
    pool_pre_ping=True,   # 执行前校验连接有效性
    pool_timeout=10       # 10秒内获取不到连接抛超时
)

# 初始化数据库
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# 依赖项
def session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def context():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()