from abc import ABC
from typing import Generic, TypeVar

from src.app.repositories.base_repository import BaseRepository

RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[RepositoryType], ABC):
    def __init__(self, repository: type[RepositoryType]):
        self._repository = repository
        self._session = self._repository.get_session()

    async def rollback(self):
        await self._session.rollback()

    async def commit(self):
        await self._session.commit()
