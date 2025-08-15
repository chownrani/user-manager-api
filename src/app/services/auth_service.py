from http import HTTPStatus
from typing import Dict

from fastapi import HTTPException

from src.app.models.user import User
from src.app.repositories.user_repository import UserRepository
from src.app.security.security import create_access_token, verify_password
from src.app.services.base_service import BaseService


class AuthService(BaseService[UserRepository]):
    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def authenticate_and_create_token(
        self, email: str, password: str
    ) -> Dict[str, str]:
        user = await self._repository.get_by_email(email)

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not verify_password(password, user.password):
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        access_token = create_access_token(claims={"sub": user.email})

        return {"access_token": access_token, "token_type": "bearer"}

    async def refresh_token(self, user: User) -> Dict[str, str]:
        db_user = await self._repository.get_by_email(user.email)
        access_token = create_access_token(claims={"sub": db_user.email})

        return {"access_token": access_token, "token_type": "bearer"}
