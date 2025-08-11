from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.app.settings.settings import Settings


class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = Settings().DATABASE_URL
        self.__engine = self.__create_engine()

    def get_engine(self):
        return self.__engine

    def __create_engine(self):
        engine = create_async_engine(self.__connection_string)
        return engine

    async def get_session(self):
        async with AsyncSession(
            self.__engine, expire_on_commit=False
        ) as session:
            yield session
