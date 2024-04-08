from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.schemas import ExpenseRead
from src.api.income.schemas import SalaryRead, TipRead
from src.api.services.models import Month
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from src.api.services.crud_monthly_stats import CRUDmonth

router = APIRouter(
    prefix='/services',
    tags=['services']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get('/monthly_expense', response_model=List[ExpenseRead])
async def get_monthly_expense(month: Month = Depends(Month),
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user),
                              crud_services: CRUDmonth = Depends(CRUDmonth)):
    try:
        expenses = await crud_services.get_monthly_expense(month=month, session=session, user=user)

        if expenses == []:
            raise Exception

        return expenses

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/monthly_salary', response_model=List[SalaryRead])
async def get_monthly_salary(month: Month = Depends(Month),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user),
                             crud_services: CRUDmonth = Depends(CRUDmonth)):
    try:
        salary = await crud_services.get_monthly_salary(month=month, session=session, user=user)

        if salary == []:
            raise Exception

        return salary

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/monthly_tip', response_model=List[TipRead])
async def get_monthly_tip(month: Month = Depends(Month),
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user),
                          crud_services: CRUDmonth = Depends(CRUDmonth)):
    try:
        tip = await crud_services.get_monthly_tip(month=month, session=session, user=user)

        if tip == []:
            raise Exception

        return tip

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
