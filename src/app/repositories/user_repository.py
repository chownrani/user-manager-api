from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.user import User
from src.app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.get_by_field("email", email)

    async def get_by_username(self, username: str) -> Optional[User]:
        return await self.get_by_field("username", username)

    async def get_by_email_or_username(
        self, email: str, username: str
    ) -> Optional[User]:
        query = select(User).where(
            or_(User.email == email, User.username == username)
        )

        session = self.get_session()
        result = await session.execute(query)

        return result.scalar_one_or_none()

    async def email_already_exists(self, email: str) -> bool:
        return await self.exists(email=email)

    async def username_already_exists(self, username: str) -> bool:
        return await self.exists(username=username)

    async def email_or_username_exists(
        self, email: str, username: str
    ) -> tuple[bool, str]:
        user = await self.get_by_email_or_username(email, username)

        if user:
            if user.email == email:
                return True, "email"
            elif user.username == username:
                return True, "username"

        return False, ""
