#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023/11/8
# @Author : xm2022
# @desc : 用户表的增删改查
from typing import Any

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from crud.base import CRUDBase
from models import User, Role
from schemas.user import UserCreate, UserUpdate, UserOut
from schemas.page import PageSchema

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_all(self, db: Session, page: PageSchema, *args) -> list[UserOut | None]:
        stmt = select(self.model)
        # 获取查询结果
        result = db.execute(stmt).scalars().all()
    
        # 将结果转换为 UserOut 模型列表
        user_list = [UserOut.from_orm(user) for user in result]

        return user_list, len(user_list)

    def create(self, db: Session, obj_in: UserCreate) -> User:
        from core.security import get_password_hash
        """ 创建用户 """
        setattr(obj_in, 'password', get_password_hash(obj_in.password))
        obj_in.__dict__['role_id'] = 2
        return super().create(db, obj_in=obj_in)

    def get_user_by_name(self, db: Session, name: Any) -> User | None:
        """ 通过用户名获取用户 """
        stmt = (
            select(self.model.__table__.c)
            .where(self.model.username == name)
            .where(self.model.is_deleted == 0)
        )
        result = db.execute(stmt).first()
        return result
    
    def get_user_by_id(self, db: Session, id: Any) -> User | None:
        """ 通过ID获取用户 """
        stmt = (
            select(self.model.__table__.c)
            .where(self.model.id == id)
            .where(self.model.is_deleted == 0)
        )
        result = db.execute(stmt).first()
        return result
    
    def update_password(self, db: Session, id: int, new_password: str) -> User:
        from core.security import get_password_hash
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(password=get_password_hash(new_password))
        )
        db.execute(stmt)
        db.commit()
    
user_crud = CRUDUser(User)
