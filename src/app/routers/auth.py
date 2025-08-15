from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.dependencies.dependencies import get_auth_service
from src.app.models.user import User
from src.app.schemas.schemas import Token
from src.app.security.security import get_current_user
from src.app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=HTTPStatus.OK, response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    token_data = await auth_service.authenticate_and_create_token(
        form_data.username, form_data.password
    )
    return token_data


@router.post("/refresh_token", response_model=Token)
async def refresh_access_token(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.refresh_token(current_user)
