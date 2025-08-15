from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.database.connection import db_handler
from src.app.repositories.user_repository import UserRepository
from src.app.services.auth_service import AuthService
from src.app.services.user_service import UserService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in db_handler.get_session():
        yield session


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


def get_auth_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(repository)
