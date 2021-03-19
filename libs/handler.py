from libs.error_code import APIException
from flask_restful import HTTPException

def default_error_handler(ex):
    print(ex)
    # ex => 是一个异常
    # 如果是自己抛出的异常，则原样返回
    # raise APIException() => {message:xxx, status_code:xxx}
    if isinstance(ex, APIException):
        return ex

    # 如果是其他系统异常如404等
    if isinstance(ex, HTTPException):
        code = ex.code
        msg = ex.description
        error_code = 10004
        return APIException(msg, code, error_code)

    # 如果是其他任何未知错误，返回一个默认的错误
    else:
        # {"meassage": "opps!", "status_code": 9999}
        return APIException()