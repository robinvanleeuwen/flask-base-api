from typing import Union
from uuid import uuid4

from flask_jsonrpc import JSONRPCBlueprint
from database import db_session_manager
from helpers.response import create_json_response
from logger import CustomLogger
from models.api import Account

auth = JSONRPCBlueprint("auth", __name__)
log = CustomLogger()


def get_account_from_database(login_code: str) -> Union[Account, None]:
    with db_session_manager() as session:
        result = session.query(
            Account
        ).filter(
            Account.login_code == login_code
        ).all()

        num_records = len(result)

        if num_records == 0 or num_records > 1:
            return None
        elif len(result) == 1:
            return result[0]


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

    account = get_account_from_database(lc)
    if account is None:
        return create_json_response("error", "No Account Found")
    if account.login_secret == ls:
        login_success = True

    if login_success:
        data = create_json_response("ok", "Logged In", token=uuid4())
        log.info(data)
        return data
