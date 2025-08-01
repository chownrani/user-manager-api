from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.settings import Settings


class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = Settings().DATABASE_URL
        self.__engine = self.__create_engine()
        self.__session_factory = self.__create_session()

    def get_engine(self):
        return self.__engine

    def __create_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    def get_session(self):
        session: Session = self.__session_factory()
        try:
            yield session
        finally:
            session.close()

    def __create_session(self):
        return sessionmaker(bind=self.__engine, expire_on_commit=False)
