from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.expense.models import MoneySpinnerTable, Expense
from src.api.expense.schemas import ExpenseCreate, MoneySpinnerCreate

from src.api.income.models import Salary, Tip
from src.api.income.schemas import SalaryCreate, TipCreate

from fastapi_cache.decorator import cache


class CRUDexpense:
    @staticmethod
    @cache(expire=60)
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
    @cache(expire=60)
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


class CRUDincome:
    @staticmethod
    @cache(expire=60)
    async def get_all_salary(session: AsyncSession,
                             user):
        query = select(Salary).where(Salary.owner_id == user.id)
        query_result = await session.execute(query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def add_salary(salary: SalaryCreate,
                         session: AsyncSession,
                         user):
        new_salary = Salary(**salary.model_dump(), owner_id=user.id)

        session.add(new_salary)
        await session.commit()
        await session.refresh(new_salary)

        return new_salary

    @staticmethod
    async def delete_salary_by_id(salary_id: int,
                                  session: AsyncSession,
                                  user):
        salary = await session.get(Salary, salary_id)

        await session.delete(salary)
        await session.commit()

        return salary


class CRUDtip:
    @staticmethod
    async def add_tip(tip: TipCreate,
                      session: AsyncSession,
                      user):
        new_tip = Tip(**tip.model_dump(), owner_id=user.id)

        session.add(new_tip)
        await session.commit()
        await session.refresh(new_tip)

        return new_tip

    @staticmethod
    @cache(expire=60)
    async def get_all_tips(session: AsyncSession,
                           user):
        query = select(Tip).where(Tip.owner_id == user.id)
        query_result = await session.execute(query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def delete_tip_by_id(tip_id: int,
                               session: AsyncSession,
                               user):
        tip = await session.get(Salary, tip_id)

        await session.delete(tip)
        await session.commit()

        return tip
