from database import db_session_manager
from models.api import Account, Token


def get_token_by_login_code(login_code):
    with db_session_manager() as session:
        r = session.query(Account, Token).filter(Account.login_code == login_code).filter(Account.id == Token.id).all()

