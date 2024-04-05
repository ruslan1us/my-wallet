from fastapi_users import FastAPIUsers
from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.models import Expense
from src.api.expense.schemas import ExpenseRead
from src.api.income.models import Salary, Tip
from src.api.income.schemas import SalaryRead
from src.database import get_async_session

from src.api.services.models import Month

from typing import List


router = APIRouter(
    prefix='/services',
    tags=['services']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get('/monthly_expense_stats', response_model=List[ExpenseRead])
async def get_monthly_expense_stats(month: Month = Depends(Month),
                                     session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    month = month.model_dump()
    expense_query = select(Expense).where(month.get('month') == func.date_part('month', Expense.expensed_at),
                                          Expense.owner_id == user.id)

    query_result = await session.execute(expense_query)
    result = query_result.scalars().all()

    return result


@router.get('/monthly_salary_stats', response_model=List[SalaryRead])
async def get_monthly_salary_stats(month: Month = Depends(Month),
                                   session: AsyncSession = Depends(get_async_session),
                                   user: User = Depends(current_user)):
    month = month.model_dump()
    salary_query = select(Salary).where(month.get('month') == func.date_part('month', Salary.date),
                                        Salary.owner_id == user.id)

    query_result = await session.execute(salary_query)
    result = query_result.scalars().all()

    return result


@router.get('/monthly_tip_stats')
async def get_monthly_tip_stats(month: Month = Depends(Month),
                                session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_user)):
    month = month.model_dump()
    tip_query = select(Tip).where(month.get('month') == func.date_part('month', Tip.date),
                                  Tip.owner_id == user.id)

    query_result = await session.execute(tip_query)
    result = query_result.scalars().all()

    return result
