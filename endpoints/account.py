from bcrypt import gensalt, hashpw
from flask_jsonrpc import JSONRPCBlueprint
from database import db_session_manager
from helpers.response import Response
from logger import CustomLogger
from models.api import Token, Account

account = JSONRPCBlueprint("account", __name__)
log = CustomLogger()


def get_account_info_by_token(key: str) -> Response:
    with db_session_manager() as s:

        try:
            token_record = s.query(Token).filter(Token.key == key).one()
        except Exception as e:
            return Response(code="error", message="token not present")

        try:
            account_record = s.query(Account).filter(Account.id == token_record.account_id).one()
        except Exception as e:
            return Response(code="error", message="account not present")

        account_info = {
            "uid": account_record.uid,
            "login_code": account_record.login_code,
            "admin_level": account_record.admin_level,
        }

        return Response(code="ok", message="account info retrieved", **account_info)


@account.method("create_account")
def create_account(
        token: str,
        login_code: str,
        login_secret_1: str = "",
        login_secret_2: str = "",
        admin_level: int = 0
) -> dict:
    account_info_response = get_account_info_by_token(token)

    if account_info_response.code == "error":
        return Response(code="error", message="no account for token", error=account_info_response.message).to_json()

    if account_info_response.code == "ok":
        account_info = account_info_response.optional_fields

        if account_info.get("admin_level", "0") < admin_level:
            return Response(
                code="error",
                message="admin_level not sufficient",
                help=f"user with level {account_info.get('admin_level')} cannot create account with level {admin_level}"
            ).to_json()

    if login_code == "":
        return Response(code="error", message="login code empty").to_json()

    if login_secret_1 == "" or login_secret_2 == "":
        return Response(code="error", message="password empty").to_json()
    elif login_secret_1 != login_secret_2:
        return Response(code="error", message="passwords do not match").to_json()

    with db_session_manager() as s:

        salt = gensalt()
        hashed_password = hashpw(password=login_secret_1.encode(), salt=salt)

        new_account = Account()
        new_account.login_code = login_code
        new_account.login_secret = hashed_password
        new_account.admin_level = admin_level
        s.add(new_account)

        try:
            s.commit()
            log.info("New account saved")
        except Exception as e:
            return Response(
                code="error",
                message="failure saving account",
                help=str(e)
            ).to_json()

        return Response(code="ok", message="new account created", login_code=login_code).to_json()

# @account.method("get_accounts")
# def get_accounts()
