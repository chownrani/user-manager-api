from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from src.app.models.user import User
from src.app.repositories.user_repository import UserRepository
from src.app.schemas.schemas import FilterPage, UserSchema
from src.app.security.security import get_password_hash
from src.app.services.base_service import BaseService


class UserService(BaseService[UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def create_user(self, user_data: UserSchema) -> User:
        exists, field = await self._repository.email_or_username_exists(
            user_data.email, user_data.username
        )

        if exists:
            if field == "email":
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Email already exists",
                )
            elif field == "username":
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail="Username already exists",
                )

        user_dict = user_data.model_dump()
        user_dict["password"] = get_password_hash(user_data.password)

        return await self._repository.create(user_dict)

    async def get_users(self, filter_params: FilterPage) -> List[User]:
        return await self._repository.get_all(
            offset=filter_params.offset,
            limit=filter_params.limit,
        )

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found",
            )

        return user

    async def get_user_by_email(self, user_email: str) -> User:
        user = await self._repository.get_by_email(user_email)

        return user

    async def authenticate_user(self, user_email: str) -> Optional[User]:
        return await self._repository.get_by_email(user_email)

    async def update_user(
        self, user_id: int, user_data: UserSchema, current_user: User
    ) -> User:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not enough permissions",
            )

        try:
            updated_data = user_data.model_dump()
            updated_data["password"] = get_password_hash(user_data.password)

            updated_user = await self._repository.update(
                current_user, updated_data
            )
            return updated_user

        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail="Username or email already exists",
            )

    async def delete_user(self, user_id: int, current_user: User) -> bool:
        if current_user.id != user_id:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail="Not enough permissions",
            )

        user = await self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="User not found",
            )

        return await self._repository.delete(user)
