import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

if os.environ["DATABASE_URL"] is None:
    pass
APIBase = declarative_base()

SessionMaker = sessionmaker(
    autocommit=False,
    autoflush=True
)

SessionMaker.configure(
    binds={
        APIBase: create_engine(url=os.environ["DATABASE_URL"], pool_size=15, max_overflow=5)
    }
)


@contextmanager
def db_session_manager():
    db_session = SessionMaker()
    try:
        yield db_session
    except Exception as e:
        db_session.rollback()
        raise e
    finally:
        db_session.close()
