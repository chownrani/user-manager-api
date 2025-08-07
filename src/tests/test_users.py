from http import HTTPStatus

from fastapi.testclient import TestClient

from src.app.models.models import User
from src.app.schemas.schemas import Token, UserPublic


def test_create_user(client: TestClient):
    response = client.post(
        "/users",
        json={
            "username": "rani",
            "email": "rani@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "rani",
        "email": "rani@example.com",
        "id": 1,
    }


def test_create_username_already_exists(client: TestClient, user: User):
    response = client.post(
        "/users",
        json={
            "username": user.username,
            "email": "rani@example.com",
            "password": "secret",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_email_already_exists(client: TestClient, user: User):
    response = client.post(
        "/users",
        json={"username": "rani", "email": user.email, "password": "secret"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_users(client: TestClient, user: User, token: Token):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(
        "/users", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.json() == {"users": [user_schema]}


def test_read_user_by_id(client: TestClient, user: User, token: Token):
    response = client.get(
        f"/users/{user.id}", headers={"Authorization": f"Bearer {token}"}
    )
    user_data = UserPublic.model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert user_data.id == user.id
    assert user_data.username == user.username
    assert user_data.email == user.email


def test_read_user_by_id_not_found(client: TestClient, token: Token):
    response = client.get(
        "/users/999", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client: TestClient, user: User, token: Token):
    response = client.put(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "arthur",
            "email": "arthur@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "arthur",
        "email": "arthur@example.com",
        "id": 1,
    }


def test_integrity_error(client: TestClient, user: User, token: Token):
    client.post(
        "/users",
        json={
            "username": "gabriel",
            "email": "gabriel@example.com",
            "password": "secret",
        },
    )

    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "gabriel",
            "email": "arthur@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username or email already exists"}


def test_delete_user(client: TestClient, user: User, token: Token):
    response = client.delete(
        "/users/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}
