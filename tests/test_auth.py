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


test_user = {"username": "string", "password": "string"}


def test_login():
    response = client.post("/auth/jwt/login", data=test_user)
    token = response.cookies.get('my_wallet_cookie')
    assert response.status_code == 204
    return token
