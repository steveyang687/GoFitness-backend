from libs.error_code import Success


def generate_response(data=None, message=Success.message,
                      status_code=Success.status_code, **kwargs):
    if data is None:
        data = []
    return {
        "message": message,
        "status_code": status_code,
        "data": data,
        **kwargs
    }
