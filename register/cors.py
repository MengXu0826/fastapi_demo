# -*- coding: utf-8 -*-
# @Time : 2024/10/23
# @Author : xm2022
# @desc : 解决跨域请求
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings


def register_cors(app: FastAPI):
    """ 跨域请求 -- https://fastapi.tiangolo.com/zh/tutorial/cors/ """

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )