# -*- coding: utf-8 -*-
# @Time : 2024/10/23
# @Author : xm2022
# @desc : 注册路由
from fastapi import FastAPI, Depends

from apis import public, user
from core.config import settings

def register_router(app: FastAPI):
    """ 注册路由 """

    app.include_router(public.router, prefix=settings.API_PREFIX, tags=["Public"])

    app.include_router(user.router, prefix=settings.API_PREFIX + "/user", tags=["User"])