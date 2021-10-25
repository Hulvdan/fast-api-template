import logging
import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.testclient import TestClient

logger = logging.getLogger("fixture")
logger.setLevel(logging.INFO)


def pytest_sessionstart(session):
    os.environ.setdefault("TEST_RUN", "1")
    from main import app

    _create_database(app.config.SQLALCHEMY_DATABASE_URI)
    _create_database_connection(app)


def pytest_sessionfinish(session):
    os.environ.setdefault("TEST_RUN", "1")
    from main import app

    _delete_database(app.config.SQLALCHEMY_DATABASE_URI)


def _create_database(dsn):
    database_name = dsn.split("/")[-1]
    logger.info("check database {}".format(database_name))

    db_exists = database_exists(dsn)
    if db_exists:
        logger.warning("drop old database {}".format(database_name))
        drop_database(dsn)

    logger.info("create new database {}".format(database_name))
    create_database(dsn)


@pytest.fixture(scope="class")
def get_session_and_client_fixture(request):
    from main import app

    # Set TEST_RUN environment to tell app that we are running under test environment to connect dummy test
    os.environ.setdefault("TEST_RUN", "1")

    from core.db.base import Base

    engine = create_engine(app.config.SQLALCHEMY_DATABASE_URI)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)()

    request.cls.session = session
    request.cls.client = TestClient(app)
    request.cls.Base = Base


def _delete_database(dsn):
    database_name = dsn.split("/")[-1]
    logger.info("drop old database {}".format(database_name))
    drop_database(dsn)


def _create_database_connection(app):
    from core.db.base import Base

    engine = create_engine(app.config.SQLALCHEMY_DATABASE_URI)
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)()

    import subprocess

    subprocess.call("cd {} && sh scripts/migrate.sh head".format(app.config.BASE_DIR), shell=True)
    return session, Base
