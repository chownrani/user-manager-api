from abc import ABC
from typing import Any, Generic, List, Optional, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType], ABC):
    def __init__(self, model: type[ModelType], session: AsyncSession):
        self._model = model
        self._session = session

    def get_session(self) -> AsyncSession:
        return self._session

    async def create(self, data: dict) -> ModelType:
        db_obj = self._model(**data)

        self._session.add(db_obj)
        await self._session.commit()
        await self._session.refresh(db_obj)

        return db_obj

    async def get_all(
        self, *, offset: int = 0, limit: int = 100
    ) -> List[ModelType]:
        query = select(self._model).offset(offset).limit(limit)
        result = await self._session.execute(query)

        return result.scalars().all()

    async def get_by_id(self, obj_id: Any) -> Optional[ModelType]:
        return await self._session.get(self._model, obj_id)

    async def get_by_field(
        self, field: str, value: Any
    ) -> Optional[ModelType]:
        query = select(self._model).where(getattr(self._model, field) == value)
        result = await self._session.execute(query)

        return result.scalar_one_or_none()

    async def update(
        self, db_obj: type[ModelType], update_data: dict
    ) -> ModelType:
        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await self._session.commit()
        await self._session.refresh(db_obj)

        return db_obj

    async def delete(self, db_obj: type[ModelType]) -> bool:
        await self._session.delete(db_obj)
        await self._session.commit()

        return True

    async def exists(self, **kwargs) -> bool:
        conditions = []
        for key, value in kwargs.items():
            if hasattr(self._model, key):
                conditions.append(getattr(self._model, key) == value)

        if conditions:
            query = select(self._model).where(*conditions)
            result = await self._session.execute(query)
            return result.scalar_one_or_none is not None

        return False
