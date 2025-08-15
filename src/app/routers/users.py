from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from src.app.dependencies.dependencies import get_user_service
from src.app.models.user import User
from src.app.schemas.schemas import (
    FilterPage,
    Message,
    UserList,
    UserPublic,
    UserSchema,
)
from src.app.security.security import get_current_user
from src.app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(
    user: UserSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.create_user(user)
    return user


@router.get("/", status_code=HTTPStatus.OK, response_model=UserList)
async def read_users(
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    filter_users: Annotated[FilterPage, Query()],
):
    users = await user_service.get_users(filter_users)
    return {"users": users}


@router.get("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def read_user_by_id(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get_user_by_id(user_id)
    return user


@router.put("/{user_id}", status_code=HTTPStatus.OK, response_model=UserPublic)
async def update_user(
    user_id: int,
    user: UserSchema,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    updated_user = await user_service.update_user(user_id, user, current_user)
    return updated_user


@router.delete("/{user_id}", status_code=HTTPStatus.OK, response_model=Message)
async def delete_user(
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    await user_service.delete_user(user_id, current_user)
    return {"message": "User deleted"}
