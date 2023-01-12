# -*- coding: utf-8 -*-

from db.orm import Base
from fastapi.testclient import TestClient
from pytest import MonkeyPatch
from pytest import fixture as pytest__fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./tests.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def override__get__database() -> sessionmaker:
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        database.close()


Base.metadata.create_all(bind=engine)


@pytest__fixture
def _client(monkeypatch: MonkeyPatch) -> TestClient:
    from utils import database  # pylint:disable=import-outside-toplevel

    monkeypatch.setattr(database, "get__database", override__get__database)

    from settings import active  # pylint:disable=import-outside-toplevel

    monkeypatch.setattr(
        active,
        "STATIC_DIR",
        "/code/app/static",
    )
    monkeypatch.setattr(
        active,
        "TEMPLATES_DIR",
        "/code/app/templates",
    )

    from main import app  # pylint:disable=import-outside-toplevel

    return TestClient(app)


@pytest__fixture
def session() -> sessionmaker:
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        database.close()
