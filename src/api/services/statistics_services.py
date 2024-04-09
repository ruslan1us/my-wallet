from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.api.expense.models import Expense
from src.api.income.models import Salary, Tip


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
