# -*- coding: utf-8 -*-
# @Time : 2024/09/08
# @Author : xm2022
# @desc : 表结构(只测试了MySQL)
"""
参考文档:
    [1]: https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping
    [2]: https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#mapper-configuration-options-with-declarative
    [3]: https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html#composing-mapped-hierarchies-with-mixins
    [4]: https://docs.sqlalchemy.org/en/20/orm/declarative_config.html#other-declarative-mapping-directives
"""
import re
from datetime import datetime

from sqlalchemy import String, Integer, SmallInteger, ForeignKey, func, text, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship, Mapped, declared_attr
from typing_extensions import Annotated

idPk = Annotated[int, mapped_column(primary_key=True, autoincrement=True, comment="主键ID")]


class Base(DeclarativeBase):
    """ ORM 基类 | 详见[1]、[3]"""
    __table_args__ = {
        "mysql_engine": "InnoDB",  # MySQL引擎
        "mysql_charset": "utf8mb4",  # 设置表的字符集
        "mysql_collate": "utf8mb4_general_ci",  # 设置表的校对集
        # "mysql_comment": "表名备注",  # 设置表名备注
    }

    # 驼峰命名转为小写下划线命名: https://blog.csdn.net/mouday/article/details/90079956
    @declared_attr.directive
    def __tablename__(cls) -> str:
        snake_case = re.sub(r"(?P<key>[A-Z])", r"_\g<key>", cls.__name__)
        return snake_case.lower().strip('_')
    
class CommonMixin:
    """ 公共元素类 | 详见[4] """

    is_deleted: Mapped[int | None] = \
        mapped_column(SmallInteger, server_default=text('0'), comment="是否删除: 0 未删除 1 已删除")
    create_time: Mapped[datetime | None] = \
        mapped_column(insert_default=func.now(), comment="创建时间")
    update_time: Mapped[datetime | None] = \
        mapped_column(server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
class User(Base, CommonMixin):
    """ 用户表 """

    id: Mapped[idPk]
    username: Mapped[str] = mapped_column(String(60), unique=True, comment="用户名")
    password: Mapped[str] = mapped_column(String(64), comment="密码")
    avatar: Mapped[str | None] = mapped_column(String(60), comment="头像")
    phone: Mapped[str | None] = mapped_column(String(30), comment="手机号")
    
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), comment="角色ID")
    role = relationship("Role", back_populates="users")  # 一对一关系

class Role(Base, CommonMixin):
    """ 角色表 """

    id: Mapped[idPk]
    name: Mapped[str] = mapped_column(String(32), comment="角色名称")
    code: Mapped[str] = mapped_column(String(32), comment="角色code")
    description: Mapped[str | None] = mapped_column(String(60), comment="角色描述")

    users = relationship("User", back_populates="role")  # 一对多，但每用户仅对应一个角色
