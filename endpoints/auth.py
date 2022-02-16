from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

from flask_jsonrpc import JSONRPCBlueprint
from sqlalchemy.orm import Session

from database import db_session_manager
from getuid import generate_uid
from helpers.response import Response
from helpers.token import generate_api_token
from logger import CustomLogger
from models.api import Account, Token

auth = JSONRPCBlueprint("auth", __name__)
log = CustomLogger()

EXPIRATION_ATTRIBUTE = "days"  # Timedelta: weeks, days, hours, minutes or seconds.
TOKEN_EXPIRATION_DELTA = 1  # Tokens are invalid after (x) EXPIRATION_ATTRIBUTE.


def get_account_from_database(login_code: str) -> Union[Account, None]:
    with db_session_manager() as session:
        result = session.query(
            Account
        ).filter(
            Account.login_code == login_code
        ).all()

        num_records = len(result)

        log.debug(f"get_account_from_database: accounts found {num_records}")

        if num_records == 0 or num_records > 1:
            return None
        elif len(result) == 1:
            return result[0]


def clear_expired_tokens_for_account(account: Account):
    """
    Get all the tokens in the database for the given account.
    If the token is expired, delete it from the database.
    :param account: The Account object for which to get the tokens for.
    :return: Nothing
    """
    with db_session_manager() as s:
        result = s.query(Token).filter(Token.account_id == account.id).all()

        count = 0
        for token in result:
            if datetime.now() - timedelta(**{EXPIRATION_ATTRIBUTE: TOKEN_EXPIRATION_DELTA}) > token.valid_until:
                # token has expired, delete it.
                log.debug(f"token.id {token.id} has expired. Deleting token.")
                s.delete(token)
                count += 1
        try:
            s.commit()
        except Exception as e:
            raise Exception(f"Could not delete expired tokens for account '{account.login_code}', {str(e)}")

        log.debug(f"Cleared {count} token(s)")


def extend_token_lifetime(s: Session, token: Token) -> Response:
    """
    Extend the lifetime for the token with TOKEN_EXPIRATION_DELTA

    :param s: SQLAlchemy Session
    :param token:
    :return: Response
        ok: "lifetime extended"
        error: "failed to extend lifetime"
    """

    token.valid_until = token.valid_until + timedelta(**{EXPIRATION_ATTRIBUTE: TOKEN_EXPIRATION_DELTA})
    s.add(token)
    try:
        log.debug("Extending token lifetime")
        s.commit()
        return Response(code="ok", message="lifetime extended")
    except Exception as e:
        return Response(code="error", message="failed to extend lifetime")


def check_token_for_account(account: Account) -> Response:
    """
    Check if there is a token in the database for the
    given account. If there is a token, check it's expiration
    datetime. Extend it if the token is still valid or create
    a new token if the current token has expired.

    :param account: Account object of the account to be checked
    :return: Response
        ok: token lifetime extended
        ok: token created
        error: store token failure

    """

    clear_expired_tokens_for_account(account)

    with db_session_manager() as s:
        # We'll use the first token if there are more than one
        token = s.query(Token).filter(Token.account_id == account.id).first()

        # If there are no tokens, create a new one for the account.
        if token is None:
            new_token = Token()
            new_token.key = generate_api_token()
            new_token.valid_until = datetime.now() + timedelta(**{EXPIRATION_ATTRIBUTE: TOKEN_EXPIRATION_DELTA})
            new_token.account_id = account.id
            new_token.uid = generate_uid()
            s.add(new_token)
            try:
                s.commit()
                log.debug("Created new token")
                return Response(code="ok", message="token created", api_key=new_token.key)
            except Exception as e:
                return Response(code="error", message="store token failure")
        else:
            response = extend_token_lifetime(s, token)
            if response.code == "ok":
                return Response(code="ok", message="token lifetime extended", api_key=token.key)
            else:
                return response


@auth.method("login")
def login(lc: str, ls: str) -> dict:
    """
    Do the authentication process
    :param lc: login code
    :param ls: login secret
    :return: JSON Response
    """
    log.debug("Starting Authentication Process")

    account = get_account_from_database(lc)
    if account is None:
        return Response("error", "No Account Found").to_json()
    if account.login_secret == ls:
        login_success = True
    else:
        return Response("error", "invalid credentials").to_json()

    response = check_token_for_account(account)
    if response.code == "ok":
        key = response.optional_fields.get("api_key")
    else:
        return Response(
            code="error",
            message="failed to create or update token for account"
        ).to_json()

    if login_success:
        val = Response("ok", "logged in", api_key=key).to_json()
        log.debug(val)
        return val
