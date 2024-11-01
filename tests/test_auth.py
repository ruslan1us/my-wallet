import pytest

from conftest import client


def test_register():
    response = client.post('/auth/register', json={
        "email": "string",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "string"
    })

    assert response.status_code == 201


@pytest.fixture(scope="module")
def test_user():
    return {"username": "string", "password": "string"}


def test_login(test_user):
    response = client.post("/auth/jwt/login", data=test_user)
    assert response.status_code == 204
