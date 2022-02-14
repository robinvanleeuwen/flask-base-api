from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

from flask_jsonrpc import JSONRPCBlueprint
from database import db_session_manager
from getuid import generate_uid
from helpers.response import Response
from logger import CustomLogger
from models.api import Account, Token

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


def store_token_for_account(login_code: str, token: str) -> Response:
    with db_session_manager() as s:
        account = s.query(Account).filter(Account.login_code == login_code).first()

        if account is None:
            return Response("err", "account not found in database")

        t = Token()
        t.token = token
        t.uid = generate_uid()
        t.valid_until = datetime.now() + timedelta(days=1)
        t.account = account
        s.add(t)

        # noinspection PyBroadException
        try:
            s.commit()
        except Exception as e:
            return Response("err", "Exception inserting token in database")

        return Response("ok", "token stored in database")


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
        return Response("error", "No Account Found").to_json()
    if account.login_secret == ls:
        login_success = True

    token = lt
    if token is None:
        token = str(uuid4())
        store_token_for_account(account, token)

    if login_success:
        return Response("ok", "logged in", token=token).to_json()

    return Response("error", "invalid credentials", token=token).to_json()
