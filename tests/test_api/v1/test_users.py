import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings


def test_create_user(client: TestClient, db: Session) -> None:
    data = {
        "email": "test@example.com",
        "password": "password",
        "full_name": "Test User"
    }
    response = client.post(
        f"{settings.API_V1_STR}/users/", json=data,
    )
    assert response.status_code == 200
    created_user = response.json()
    assert created_user["email"] == data["email"]
    assert created_user["full_name"] == data["full_name"]
    assert "id" in created_user


def test_get_users(client: TestClient, normal_user, db: Session) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    assert users[0]["email"] == normal_user.email


def test_get_user(client: TestClient, normal_user, db: Session) -> None:
    
    response = client.get(f"{settings.API_V1_STR}/users/{normal_user.id}")
    assert response.status_code == 200
    user = response.json()
    assert user["email"] == normal_user.email


def test_update_user(client: TestClient, normal_user, db: Session) -> None:
    data = {
        "full_name": "Updated Name"
    }
    response = client.put(
        f"{settings.API_V1_STR}/users/{normal_user.id}", json=data,
    )
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["full_name"] == data["full_name"]


def test_delete_user(client: TestClient, normal_user, db: Session) -> None:
    response = client.delete(f"{settings.API_V1_STR}/users/{normal_user.id}")
    assert response.status_code == 200

    # ユーザーが削除されたことを確認
    response = client.get(f"{settings.API_V1_STR}/users/{normal_user.id}")
    assert response.status_code == 404
