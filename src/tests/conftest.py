from contextlib import contextmanager
from datetime import datetime
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.app.database.connection import db_handler
from src.app.models.models import Base, User
from src.app.routers.app import app
from src.app.security.security import get_password_hash
from src.app.settings.settings import Settings


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)

    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[db_handler.get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = "testtest"

    user = User(
        username="Teste",
        email="teste@test.com",
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.plain_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.plain_password},
    )
    return response.json()["access_token"]


@pytest.fixture
def credentials_exception():
    return {
        "status_code": HTTPStatus.UNAUTHORIZED,
        "detail": "Could not validate credentials",
        "headers": {"WWW-Authenticate": "Bearer"},
    }


@pytest.fixture
def settings():
    return Settings()
