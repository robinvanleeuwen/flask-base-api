from uuid import uuid4

from flask import g
from flask_jsonrpc import JSONRPCBlueprint

from helpers.response import create_json_response
from logger import CustomLogger

auth = JSONRPCBlueprint("auth", __name__)
log = CustomLogger()


@auth.method("login")
def login(lc: str, ls: str, lt: str) -> dict:
    """
    Do the authentication process
    :param lc: login code
    :param ls: login secret
    :param lt: login token
    :return: JSON Response
    """
    log.info("Starting Authentication Process")

    login_success = False

    if lc == "c" and ls == "s" and lt == "t":
        log.info("Login Success")
        login_success = True
        g.lc = lc

    if login_success:
        data = create_json_response("ok", "Logged In", token=uuid4())
        log.info(data)
        return data
    else:
        log.fail("Login failed")
        return create_json_response("error", "Wrong Credentials")
