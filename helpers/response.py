from logger import CustomLogger

log = CustomLogger()


def create_json_response(code: str, message: str, **kwargs) -> dict:
    default_args = {
        "code": code,
        "message": message
    }
    if len(list({**kwargs})) > 0:
        data = {**default_args, **kwargs}
        return data
    else:
        return default_args
