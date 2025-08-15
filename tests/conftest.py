from contextlib import contextmanager
from datetime import datetime
from http import HTTPStatus

import factory
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from src.app.database.connection import db_handler
from src.app.dependencies.dependencies import (
    get_auth_service,
    get_user_repository,
    get_user_service,
)
from src.app.models.user import Base, User
from src.app.repositories.user_repository import UserRepository
from src.app.routers.app import app
from src.app.security.security import get_password_hash, verify_password
from src.app.services.auth_service import AuthService
from src.app.services.user_service import UserService
from src.app.settings.settings import Settings


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"test{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")


@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    def get_user_repository_override():
        return UserRepository(session)

    def get_auth_service_override():
        user_repository = UserRepository(session)
        return AuthService(user_repository)

    def get_user_service_override():
        user_repository = UserRepository(session)
        return UserService(user_repository)

    app.dependency_overrides[db_handler.get_session] = get_session_override
    app.dependency_overrides[get_user_repository] = (
        get_user_repository_override
    )
    app.dependency_overrides[get_auth_service] = get_auth_service_override
    app.dependency_overrides[get_user_service] = get_user_service_override

    with TestClient(app) as client:
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


@pytest_asyncio.fixture
async def user(session):
    password = "testtest"

    user = User(
        username="testuser",
        email="testuser@test.com",
        password=get_password_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.plain_password = password

    return user


@pytest_asyncio.fixture
async def other_user(session):
    password = "testtest"

    user = User(
        username="otheruser",
        email="otheruser@test.com",
        password=get_password_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

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


@pytest_asyncio.fixture
async def debug_user(session):
    password = "debug123"

    user = User(
        username="debuguser",
        email="debug@test.com",
        password=get_password_hash(password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    user.plain_password = password

    assert verify_password(password, user.password), (
        "Password verification failed!"
    )

    return user
