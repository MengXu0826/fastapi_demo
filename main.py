# -*- coding: utf-8 -*-
# @Time : 2024/10/23
# @Author : xm2022
import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.init_db import init_table, init_data
from register.cors import register_cors
from register.router import register_router
from common.custom_log import my_logger

app = FastAPI(description=settings.PROJECT_DESC, version=str(settings.PROJECT_VERSION))

register_cors(app)  # 注册跨域请求

register_router(app)  # 注册路由

init_table()  # 初始化表
init_data()  # 初始化表数据
my_logger.info("项目启动成功！！！")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
    # uvicorn.run(app, host="0.0.0.0", port=8688)