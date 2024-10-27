# -*- coding: utf-8 -*-
# @Time : 2024/10/25
# @Author : xm2022
# @desc : 用户接口
from fastapi import APIRouter
from datetime import timedelta
from starlette.responses import Response
from common.depends import GetDB, PageQuery
from common.result import ResultSchema, Result
from core.security import verify_password, create_access_token
from crud import user_crud
from core.status import StatusCode, StatusMessage
from schemas.user import UserOut, UserLogin, UserPassUpdate
from core.config import settings

router = APIRouter()

@router.post("/login")
async def user_login(user: UserLogin, response: Response, db: GetDB) -> ResultSchema[UserOut]:
    """ 登录 """
    user_schema = user_crud.get_user_by_name(db, user.username)  # 获取用户信息
    if user_schema:
        if verify_password(user.password, user_schema.password):
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(subject=user_schema.id, expires_delta=access_token_expires)
            response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)  # 设置cookie，保持登录状态

            return Result.success(data=UserOut.from_orm(user_schema), code=StatusCode.OK, msg=StatusMessage.LOGIN_SUCCESSFUL)
        else:
            return Result.fail(code=StatusCode.UNAUTHORIZED, msg=StatusMessage.INVALID_PASSWORD)
    else:
        return Result.fail(code=StatusCode.UNAUTHORIZED, msg=StatusMessage.USER_NOT_FOUND)

@router.post("/register")
async def user_signup(user: UserLogin, response: Response, db: GetDB) -> ResultSchema[UserOut]:
    """ 注册 """
    user_schema = user_crud.get_user_by_name(db, user.username)  # 获取用户信息
    if user_schema:
        return Result.fail(code=StatusCode.CONFLICT, msg=StatusMessage.USER_ALREADY_EXISTS)
    else:
        user_obj = user_crud.create(db, user)  # 创建用户
        user_schema = UserOut.from_orm(user_obj)

        return Result.success(data=UserOut.from_orm(user_schema), code=StatusCode.CREATED, msg=StatusMessage.USER_REGISTERED_SUCCESSFULLY)


@router.post("/logout")
async def user_logout(response: Response) -> ResultSchema:
    """ 退出登录 """
    #Todo 销毁加密token
    return Result.success(code=StatusCode.OK, msg=StatusMessage.LOGOUT_SUCCESSFUL)


# @router.get("/list", dependencies=[Depends(check_permission(["sys:user:list"]))])
@router.get("/list")
async def users(db: GetDB, page: PageQuery) -> ResultSchema[list[UserOut]]:
    """ 获取用户列表 """
    users_obj, total = user_crud.get_all(db=db, page=page)
    return Result.success(data=users_obj, total=total, code=StatusCode.OK, msg=StatusMessage.GET_LIST_SUCCESSFUL)

@router.post("/update_password")
async def user_update_password(user: UserPassUpdate, response: Response, db: GetDB) -> ResultSchema[UserOut]:
    user_schema = user_crud.get_user_by_id(db, user.id)  # 获取用户信息
    if user_schema:
        if verify_password(user.password, user_schema.password):
            user_crud.update_password(db, user.id, user.new_password)
            return Result.success(code=StatusCode.OK, msg=StatusMessage.UPDATE_PASSWORD_SUCCESSFUL)
        else:
            return Result.fail(code=StatusCode.UNAUTHORIZED, msg=StatusMessage.INVALID_PASSWORD)
    else:
        return Result.fail(code=StatusCode.UNAUTHORIZED, msg=StatusMessage.USER_NOT_FOUND)