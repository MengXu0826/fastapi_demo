# -*- coding: utf-8 -*-
# @Time : 2023/11/8
# @Author : xm2022
# @desc : 页码模型
from pydantic import BaseModel


class PageSchema(BaseModel):
    """ 分页查询参数 """
    page: int = 1
    page_size: int = 10
