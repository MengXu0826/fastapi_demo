# -*- coding: utf-8 -*-
# @Time : 2023/09/08
# @Author : xm2022
# @desc : 响应的数据模型与数据结构
from typing import Any, TypeVar, Generic
from core.status import StatusMessage, StatusCode
from pydantic import BaseModel

T = TypeVar("T")  # 泛型 T ：https://docs.pydantic.dev/usage/models/#generic-models


class ResultSchema(BaseModel, Generic[T]):
    """ 结果数据模型 """
    code: StatusCode
    data: T | list[T] | None
    total: int | None
    msg: StatusMessage | None


class Result:
    """ 结果数据结构 """

    @staticmethod
    def success(*, code: StatusCode = StatusCode.OK, data: T = None, total: int = 0, msg: StatusMessage = None) -> ResultSchema[T]:
        """ 成功响应数据结构 """
        return ResultSchema(code=code, data=data, total=total, msg=msg)

    @staticmethod
    def fail(*, code: StatusCode = StatusCode.INTERNAL_SERVER_ERROR, data: Any = None, msg: str = None) -> ResultSchema[T]:
        """ 失败响应数据结构 """
        return ResultSchema(code=code, data=data, msg=msg, total=None)
