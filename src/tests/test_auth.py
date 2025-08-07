from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app.models.models import User


def test_login_for_access_token(client: TestClient, user: User):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.plain_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
