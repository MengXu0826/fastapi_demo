from enum import Enum

class StatusCode(Enum):
    # 成功状态码
    OK = 200
    CREATED = 201
    ACCEPTED = 202

    # 用户相关状态码
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409

    # 服务器错误状态码
    INTERNAL_SERVER_ERROR = 500

class StatusMessage(Enum):
    # 成功状态消息
    USER_REGISTERED_SUCCESSFULLY = "注册成功"
    LOGIN_SUCCESSFUL = "登陆成功"
    GET_LIST_SUCCESSFUL = "获取列表成功"
    ANALYSE_SUCCESSFUL = "分析成功"
    LOGOUT_SUCCESSFUL = "注销成功"
    UPDATE_PASSWORD_SUCCESSFUL = "更改密码成功"

    # 错误状态消息
    USER_NOT_FOUND = "用户不存在"
    INVALID_PASSWORD = "用户名或密码错误"
    USER_ALREADY_EXISTS = "用户名已存在"
    INVALID_DATA_FORMAT = "Invalid data format"
    ACCESS_DENIED = "Access denied"
    SERVER_ERROR = "An unexpected error occurred"
