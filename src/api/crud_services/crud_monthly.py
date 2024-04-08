from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.api.expense.models import Expense
from src.api.income.models import Salary, Tip


class CRUDmonth:
    @staticmethod
    async def get_monthly_expense(month,
                                  session: AsyncSession,
                                  user):
        month = month.model_dump()
        expense_query = select(Expense).where(month.get('month') == func.date_part('month', Expense.expensed_at),
                                              Expense.owner_id == user.id)

        query_result = await session.execute(expense_query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def get_monthly_salary(month,
                                 session: AsyncSession,
                                 user):
        month = month.model_dump()
        salary_query = select(Salary).where(month.get('month') == func.date_part('month', Salary.date),
                                            Salary.owner_id == user.id)

        query_result = await session.execute(salary_query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    async def get_monthly_tip(month,
                              session: AsyncSession,
                              user):
        month = month.model_dump()
        tip_query = select(Tip).where(month.get('month') == func.date_part('month', Tip.date),
                                      Tip.owner_id == user.id)

        query_result = await session.execute(tip_query)
        result = query_result.scalars().all()

        return result
