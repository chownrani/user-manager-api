from http import HTTPStatus

from fastapi.testclient import TestClient
from freezegun import freeze_time

from src.app.models.user import User
from src.app.schemas.schemas import Token


def test_login_for_access_token(client: TestClient, user: User):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": user.plain_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token


def test_token_expired(client: TestClient, user: User):
    with freeze_time("2025-08-13 12:00:00"):
        response = client.post(
            "/auth/login",
            data={"username": user.email, "password": user.plain_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2025-08-13 12:31:00"):
        response = client.put(
            f"/users/{user.id}",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "username": "wrongwrong",
                "email": "wrong@wrong.com",
                "password": "wrong",
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}


def test_token_inexistent_user(client: TestClient):
    response = client.post(
        "/auth/login",
        data={"username": "no_user@no_domain.com", "password": "testtest"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_wrong_password(client: TestClient, user: User):
    response = client.post(
        "/auth/login",
        data={"username": user.email, "password": "wrong_password"},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Incorrect email or password"}


def test_refresh_token(client: TestClient, token: Token):
    response = client.post(
        "/auth/refresh_token",
        headers={"Authorization": f"Bearer {token}"},
    )

    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"


def test_token_expired_dont_refresh(client: TestClient, user: User):
    with freeze_time("2025-08-13 12:00:00"):
        response = client.post(
            "/auth/login",
            data={"username": user.email, "password": user.plain_password},
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()["access_token"]

    with freeze_time("2025-08-13 12:31:00"):
        response = client.post(
            "/auth/refresh_token", headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {"detail": "Could not validate credentials"}
