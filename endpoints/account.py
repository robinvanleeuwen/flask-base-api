import random
import string
from typing import Union
from uuid import uuid4

from bcrypt import gensalt, hashpw
from flask_jsonrpc import JSONRPCBlueprint
from database import db_session_manager
from getuid import generate_uid
from logger import CustomLogger
from models.api import Account

account = JSONRPCBlueprint("account", __name__)
log = CustomLogger()


@account.method("create_account")
def create_account(login_code: str, login_secret: str = "", admin_level: int = 0):
    with db_session_manager() as session:
        uid = generate_uid()
        salt = gensalt()
