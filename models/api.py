import random
import string

from sqlalchemy import Integer, Column, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from database import APIBase


def generate_uid(count=15):
    uid = "".join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=count))
    return uid


class Account(APIBase):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True)
    uid = Column(Text, index=True, default=generate_uid)
    code = Column(Text, index=True, nullable=False)
    login_code = Column(Text, index=True, nullable=False, unique=True)
    login_secret = Column(LargeBinary, index=True, nullable=False)
    admin_level = Column(Integer, default=0)


class Token(APIBase):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True)
    uid = Column(Text, index=True, default=generate_uid)
    key = Column(Text, index=True)
    valid_until = Column(DateTime)
    account_id = Column(Integer, ForeignKey("account.id"))

    account = relationship("Account")
