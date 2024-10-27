# -*- coding: utf-8 -*-
# @Time : 2023/11/8
# @Author : xm2022
# @desc : 创建会话, 创建与删除所有表, 初始化数据
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from core.security import get_password_hash
from models import Base, User, Role
from common.custom_log import my_logger

# 文档中介绍了四种 创建会话 的方式: https://docs.sqlalchemy.org/en/20/orm/session_basics.html

# 创建表引擎
engine = create_engine(
    url=settings.DATABASE_URI,  # 数据库uri
    echo=settings.DATABASE_ECHO,  # 是否打印日志
    pool_pre_ping=True,  # 每次连接前都会检查连接是否有效
)

# 会话创建器
SessionLocal = sessionmaker(engine, expire_on_commit=False, autoflush=False)


EXCLUDED_TABLES = [] # 替换为您要排除的表名

def init_table(is_drop: bool = True):
    """ 创建 database 下的所有表 """
    if is_drop:
        drop_table()
    try:
        Base.metadata.create_all(engine, tables=[table for name, table in Base.metadata.tables.items() if name not in EXCLUDED_TABLES])
        my_logger.info("创建表成功!!!")
    except Exception as e:
        my_logger.error(f"创建表失败!!! -- 错误信息如下:\n{e}")


def drop_table():
    """ 删除 database 下的所有表 """
    try:
        Base.metadata.drop_all(engine, tables=[table for name, table in Base.metadata.tables.items() if name not in EXCLUDED_TABLES])
        my_logger.info("删除表成功!!!")
    except Exception as e:
        my_logger.error(f"删除表失败!!! -- 错误信息如下:\n{e}")


def init_data():
    """ 初始化表数据 """
    with SessionLocal() as session:
        role1 = Role(name="管理员", code="ROLE_ADMIN", description="管理员")
        role2 = Role(name="普通用户", code="ROLE_USER", description="普通用户")

        user1 = User(username="admin", password=get_password_hash("blcuicall"), role_id=1)
        user2 = User(username="user", password=get_password_hash("123456"), role_id=2)

        session.add_all([
            user1, user2,
            role1, role2
        ])

        session.commit()