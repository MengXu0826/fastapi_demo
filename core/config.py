# -*- coding: utf-8 -*-
# @Time : 2024/10/23
# @Author : xm2022
# @desc : 配置文件
from pathlib import Path
from pydantic import AnyHttpUrl
from pydantic import BaseSettings

IS_DEV = True
# IS_DEV = False  # 是否开发环境

current_path = Path().absolute().parent  # 当前路径

# https://docs.pydantic.dev/usage/settings/
class Settings(BaseSettings):
    PROJECT_DESC: str = "🎉 接口汇总 🎉"  # 描述
    PROJECT_VERSION: int | str = 1.0  # 版本
    API_PREFIX: str = "/api"  # 接口前缀

    BASE_URL: AnyHttpUrl = "http://127.0.0.1:8000"  # 开发环境(为了存放图片全路径)
    CORS_ORIGINS: list[AnyHttpUrl] = ["http://localhost:8080"]  # 跨域请求(务必指定精确ip, 不要用localhost)

    # openssl rand -hex 32
    SECRET_KEY: str = "00359f507cc1649f76e6b7826cfa3bfab635354092f5c635d9d08508dc2291d6"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60 * 60  # jwt token 有效时间

    DATABASE_URI: str = "mysql://root:Xm19980826@localhost:3306/fastapi_demo?charset=utf8"  # MySQL
    DATABASE_ECHO: bool = False  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)

    LOGGER_DIR: str = "logs"  # 日志文件夹名
    LOGGER_NAME: str = '{time:YYYY-MM-DD_HH-mm-ss}.log'  # 日志文件名 (时间格式)
    LOGGER_LEVEL: str = 'DEBUG'  # 日志等级: ['DEBUG' | 'INFO']
    LOGGER_ROTATION: str = "00:00"  # 日志分片: 按 时间段/文件大小 切分日志. 例如 ["500 MB" | "12:00" | "1 week"]
    LOGGER_RETENTION: str = "30 days"  # 日志保留的时间: 超出将删除最早的日志. 例如 ["1 days"]

    class Config:
        case_sensitive = True  # 区分大小写

class DevelopmentConfig(Settings):
    pass

class ProductionConfig(Settings):
    BASE_URL: AnyHttpUrl = "http://{server_ip}:{backend_port}"  # 生产环境(为了存放图片全路径)
    CORS_ORIGINS: list[AnyHttpUrl] = ["http://{server_ip}:{frontend_port}"]  # 跨域请求

    # 注意密码中的符号需要转换，如@变为%40
    DATABASE_URI: str = "mysql://{db_username}:{db_password}@localhost:3306/{db_name}?charset=utf8"  # MySQL
    DATABASE_ECHO: bool = True  # 是否打印数据库日志 (可看到创建表、表数据增删改查的信息)

    LOGGER_LEVEL: str = 'INFO'  # 日志等级: ['DEBUG' | 'INFO']

settings = DevelopmentConfig() if IS_DEV else ProductionConfig()