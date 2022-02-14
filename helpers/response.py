from helpers.exceptions import InvalidResponse
from logger import CustomLogger

log = CustomLogger()


class Response:

    def __init__(self, code: str, message: str, **kwargs):

        valid_codes = ["ok", "error"]

        if code not in valid_codes:
            raise InvalidResponse(f"Error code should be one of: {', '.join(valid_codes)}")

        self.code = code
        self.message = message

        if len(list({**kwargs})) > 0:
            self.optional_fields = {**kwargs}

    def to_json(self):

        mandatory_fields = {
            "code": self.code,
            "message": self.message
        }
        if len(list({**self.optional_fields})) > 0:
            return {**mandatory_fields, **self.optional_fields}
        else:
            return mandatory_fields
