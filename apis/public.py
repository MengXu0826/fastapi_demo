# -*- coding: utf-8 -*-
# @Time : 2023/11/8
# @Author : xm2022
# @desc : 默认接口
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
