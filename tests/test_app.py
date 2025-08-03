from http import HTTPStatus

from fastapi.testclient import TestClient

from app.models import User
from app.schemas import Token, UserPublic


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


def test_create_email_already_exists(client: TestClient, user: User):
    response = client.post(
        "/users",
        json={"username": "rani", "email": user.email, "password": "secret"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_user(client: TestClient):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client: TestClient, user: User):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")
    assert response.json() == {"users": [user_schema]}


def test_read_user_by_id(client: TestClient, user: User):
    response = client.get(f"/users/{user.id}")
    user_data = UserPublic.model_validate(response.json())

    assert response.status_code == HTTPStatus.OK
    assert user_data.id == user.id
    assert user_data.username == user.username
    assert user_data.email == user.email


def test_read_user_by_id_not_found(client: TestClient):
    response = client.get("/users/999")

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


def test_not_user_on_update(client: TestClient, user: User, token: Token):
    response = client.put(
        "/users/999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "username": "arthur",
            "email": "arthur@example.com",
            "password": "mynewpassword",
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


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


def test_not_user_on_delete(client: TestClient, user: User, token: Token):
    response = client.delete(
        "/users/999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_login_for_access_token(client: TestClient, user: User):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert "access_token" in token
    assert "token_type" in token
