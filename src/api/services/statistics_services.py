from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from src.api.expense.models import Expense, MoneySpinnerTable
from src.api.income.models import Salary, Tip

from src.api.time_func import get_month


class Services:
    @staticmethod
    async def get_all_expenses_amounts(month,
                                       session: AsyncSession,
                                       user):
        month = month.model_dump()
        query = (select(
                 func.sum(Expense.amount)).where(month.get('month') == func.date_part('month', Expense.expensed_at),
                                                 Expense.owner_id == user.id))

        query_result = await session.execute(query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def get_all_income_amounts(month,
                                     session: AsyncSession,
                                     user):
        month = month.model_dump()
        salary_query = (select(
                        func.sum(Salary.amount)).where(month.get('month') == func.date_part('month', Salary.date),
                                                       Salary.owner_id == user.id))

        tip_query = (select(
                     func.sum(Tip.amount)).where(month.get('month') == func.date_part('month', Tip.date),
                                                 Tip.owner_id == user.id))

        salary_query_result = await session.execute(salary_query)
        salary_result = salary_query_result.scalars().all()

        tip_query_result = await session.execute(tip_query)
        tip_result = tip_query_result.scalars().all()

        if tip_result[0] == None and salary_result[0]:
            return salary_result

        elif salary_result[0] == None and tip_result[0]:
            return tip_result

        result = salary_result[0] + tip_result[0]

        return [result]

    @staticmethod
    async def get_all_expenses_amounts_by_day(day,
                                              month,
                                              session: AsyncSession,
                                              user):
        day = day.model_dump()
        month = month.model_dump()
        query = (select(
            func.sum(Expense.amount)).where(day.get('day') == func.date_part('day', Expense.expensed_at),
                                            month.get('month') == func.date_part('month', Expense.expensed_at),
                                            Expense.owner_id == user.id))

        query_result = await session.execute(query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def get_the_biggest_expense(session: AsyncSession,
                                      user):
        query = (select(Expense)
                 .where(Expense.owner_id == user.id,
                        get_month() == func.date_part('month', Expense.expensed_at))
                 .order_by(desc(Expense.amount)).limit(1))

        query_result = await session.execute(query)
        result = query_result.scalars().unique().all()

        money_spinner_id = result[0].expense_place

        money_spinner_query = select(MoneySpinnerTable).where(MoneySpinnerTable.id == money_spinner_id)

        money_spinner_query_result = await session.execute(money_spinner_query)
        money_spinner_result = money_spinner_query_result.scalars().all()

        return [money_spinner_result, result]
