from sqlalchemy import insert

from src.api.expense.models import MoneySpinnerTable, Expense
from tests.conftest import async_session_maker, client
from tests.test_auth import test_login


async def test_money_spinner_add():
    async with async_session_maker() as session:
        stmt = insert(MoneySpinnerTable).values(
            name='biedronka',
            owner_id=1
        )
        await session.execute(stmt)
        await session.commit()


def test_money_spinner_add_post():
    token = test_login()
    response = client.post(
        '/money_spinners/',
        json={'name': 'kaufland'},
        cookies={"my_wallet_cookie": f"{token}"}
    )
    assert response.status_code == 201


def setup_money_spinner(token):
    response = client.post(
        '/money_spinners/',
        json={'name': 'zabka'},
        cookies={"my_wallet_cookie": f"{token}"}
    )
    assert response.status_code == 201


def test_money_spinner_delete():
    token = test_login()
    setup_money_spinner(token)
    response = client.delete(
        '/money_spinners/1',
        cookies={"my_wallet_cookie": f"{token}"}
    )
    assert response.status_code == 204


async def test_expense_add():
    async with async_session_maker() as session:
        stmt = insert(Expense).values(
            name='test',
            amount=23,
            expense_place=2,
            owner_id=1
        )
        await session.execute(stmt)
        await session.commit()


def test_expenses_add_post():
    token = test_login()
    response = client.post(
        '/expenses/',
        json={
            "name": "string",
            "amount": 123,
            "expense_place": 2
        },
        cookies={"my_wallet_cookie": f"{token}"}
    )

    assert response.status_code == 201

