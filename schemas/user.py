# -*- coding: utf-8 -*-
# @Time : 2024/10/25
# @Author : xm2022
# @desc : 用户表模型
from pydantic import BaseModel, Field

class UserIn(BaseModel):
    """ 共享数据模型 """
    username: str = Field(example='用户名')
    avatar: str | None = Field(example='头像')
    phone: str | None = Field(example='手机号')

class UserCreate(UserIn):
    """ 添加数据时的数据模型 """
    password: str | None = Field(max_length=60, example='密码')  # 前端返回可不带该字段

class UserUpdate(UserCreate):
    """ 更新数据的数据模型 """
    pass

class UserOut(UserIn):
    """ 查询数据的数据模型 """
    id: int
    is_deleted: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    """ 登录 """
    username: str = Field(example='用户名')
    password: str = Field(example='密码')

class UserPassUpdate(BaseModel):
    id: int
    password: str = Field(example='密码')
    new_password: str = Field(example='新密码')