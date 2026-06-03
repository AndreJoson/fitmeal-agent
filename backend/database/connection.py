"""
数据库连接配置
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import DATABASE_URL, DATABASE_ECHO

# 创建引擎
engine = create_engine(
    DATABASE_URL,
    echo=DATABASE_ECHO,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库表"""
    from database.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表已创建")


def drop_db():
    """删除所有表（谨慎使用！）"""
    from database.models import Base
    Base.metadata.drop_all(bind=engine)
    print("⚠️ 所有数据库表已删除")
