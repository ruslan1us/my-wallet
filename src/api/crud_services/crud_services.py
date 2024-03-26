from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.models import MoneySpinnerTable, Expense
from src.api.expense.schemas import ExpenseCreate, MoneySpinnerCreate

from fastapi_users import FastAPIUsers


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


class CRUDexpense:
    @staticmethod
    async def get_expenses_by_user(session: AsyncSession,
                                   user):
        query = (select(MoneySpinnerTable).options(joinedload(MoneySpinnerTable.expenses))
                 .where(MoneySpinnerTable.owner_id == user.id))
        query_result = await session.execute(query)
        result = query_result.scalars().unique().all()

        return result

    @staticmethod
    async def add_expense(expense: ExpenseCreate,
                          session: AsyncSession,
                          user):
        new_expense = Expense(**expense.model_dump(), owner_id=user.id)

        session.add(new_expense)
        await session.commit()
        await session.refresh(new_expense)

        return new_expense

    @staticmethod
    async def delete_expense_by_id(expense_id: int,
                                   session: AsyncSession,
                                   user):
        expense = await session.get(Expense, expense_id)

        await session.delete(expense)
        await session.commit()

        return expense


class CRUDmoneyspinner:
    @staticmethod
    async def get_money_spinners_by_user(session: AsyncSession,
                                         user):
        query = select(MoneySpinnerTable).where(MoneySpinnerTable.owner_id == user.id)
        query_result = await session.execute(query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def add_money_spinner(money_spinner: MoneySpinnerCreate,
                                session: AsyncSession,
                                user):
        new_money_spinner = MoneySpinnerTable(**money_spinner.model_dump(), owner_id=user.id)

        session.add(new_money_spinner)
        await session.commit()
        await session.refresh(new_money_spinner)

        return new_money_spinner

    @staticmethod
    async def delete_money_spinner_by_id(money_spinner_id: int,
                                         session: AsyncSession,
                                         user):
        money_spinner = await session.get(MoneySpinnerTable, money_spinner_id)

        await session.delete(money_spinner)
        await session.commit()

        return money_spinner
