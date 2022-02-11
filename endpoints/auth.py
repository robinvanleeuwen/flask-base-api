from flask_jsonrpc import JSONRPCBlueprint

from helpers.response import create_response
from logger import CustomLogger

auth = JSONRPCBlueprint("auth", __name__)
log = CustomLogger()


@auth.method("login")
def login(lc: str, ls: str, lt: str):
    """
    Do the authentication process
    :param lc: login code
    :param ls: login secret
    :param lt: login token
    :return: JSON Response
    """
    log.info("Starting Authentication Process")
    
    login_success = False

    if lc == "u" and ls == "P" and lt == "t":
        login_success = True

    if login_success:
        create_response("ok", "Logged In")
    else:
        create_response("error", "Wrong Credentials")
