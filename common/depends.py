# -*- coding: utf-8 -*-
# @Time : 2023/11/8
# @Author : xm2022
# @desc : 依赖项
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.page import PageSchema

# Annotated: https://fastapi.tiangolo.com/tutorial/dependencies/

def get_db():
    from core.init_db import SessionLocal
    """ 得到数据库的会话 """
    db = SessionLocal()  # 会话工厂(工厂对象帮助我们管理)
    try:
        yield db
    finally:
        db.close()

GetDB = Annotated[Session, Depends(get_db)]

def page_query(page: int = 1, page_size: int = 10):
    """ 获取查询参数 """
    return PageSchema(page=page, page_size=page_size)


PageQuery = Annotated[PageSchema, Depends(page_query)]
