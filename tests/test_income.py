from tests.conftest import client
from tests.test_auth import test_login


def test_income_add():
    token = test_login()
    response = client.post(
        '/income/',
        json={
            "name": "salary",
            "amount": 500
        },
        cookies={"my_wallet_cookie": f"{token}"}
    )

    assert response.status_code == 201


def test_income_delete():
    token = test_login()
    response = client.delete(
        '/income/1',
        cookies={"my_wallet_cookie": f"{token}"}
    )

    assert response.status_code == 204

