from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.api.expense.models import Expense
from src.api.income.models import Salary, Tip

from fastapi_cache.decorator import cache



class CRUDmonth:
    @staticmethod
    @cache(expire=60)
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
    @cache(expire=60)
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
    @cache(expire=60)
    async def get_monthly_tip(month,
                              session: AsyncSession,
                              user):
        month = month.model_dump()
        tip_query = select(Tip).where(month.get('month') == func.date_part('month', Tip.date),
                                      Tip.owner_id == user.id)

        query_result = await session.execute(tip_query)
        result = query_result.scalars().all()

        return result

class CRUDyear:
    @staticmethod
    @cache(expire=120)
    async def get_year_expense(year,
                               session: AsyncSession,
                               user):
        year = year.model_dump()
        expense_query = select(Expense).where(year.get('year') == func.date_part('year', Expense.expensed_at),
                                              Expense.owner_id == user.id)

        query_result = await session.execute(expense_query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    @cache(expire=120)
    async def get_year_salary(year,
                              session: AsyncSession,
                              user):
        year = year.model_dump()
        salary_query = select(Salary).where(year.get('year') == func.date_part('year', Salary.date),
                                            Salary.owner_id == user.id)

        query_result = await session.execute(salary_query)
        result = query_result.scalars().all()

        return result

    @staticmethod
    @cache(expire=120)
    async def get_year_tip(year,
                           session: AsyncSession,
                           user):
        year = year.model_dump()
        tip_query = select(Tip).where(year.get('year') == func.date_part('year', Tip.date),
                                      Tip.owner_id == user.id)

        query_result = await session.execute(tip_query)
        result = query_result.scalars().all()

        return result


class CRUDday:
    @staticmethod
    async def get_day_expense(day,
                              month,
                              session: AsyncSession,
                              user):
        day = day.model_dump()
        month = month.model_dump()
        expense_query = select(Expense).where(day.get('day') == func.date_part('day', Expense.expensed_at),
                                              month.get('month') == func.date_part('month', Expense.expensed_at),
                                              Expense.owner_id == user.id)

        query_result = await session.execute(expense_query)
        result = query_result.scalars().all()

        return result
