from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String, unique=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
