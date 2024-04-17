from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.schemas import ExpenseRead
from src.api.income.schemas import SalaryRead, TipRead
from src.api.services.models import Month, Day
from src.api.services.statistics_services import Services
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from src.api.crud_services.crud_monthly import CRUDmonth, CRUDday

router = APIRouter(
    prefix='/services/monthly',
    tags=['services']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get('/expense', response_model=List[ExpenseRead])
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


@router.get('/salary', response_model=List[SalaryRead])
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


@router.get('/day_expense', response_model=List[ExpenseRead])
async def get_day_expense(day: Day = Depends(Day),
                          month: Month = Depends(Month),
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user),
                          crud_services: CRUDday = Depends(CRUDday)):
    try:
        expenses = await crud_services.get_day_expense(day=day, month=month, session=session, user=user)

        if expenses == []:
            raise Exception

        return expenses

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/all_expenses_amounts')
async def all_expenses_amounts(month: Month = Depends(Month),
                               session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user),
                               services: Services = Depends(Services)):
    try:
        expenses_amount = await services.get_all_expenses_amounts(month=month, session=session, user=user)

        if expenses_amount == [None]:
            raise Exception

        return expenses_amount
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/all_income_amounts')
async def all_income_amounts(month: Month = Depends(Month),
                             session: AsyncSession = Depends(get_async_session),
                             user: User = Depends(current_user),
                             services: Services = Depends(Services)):
    try:
        income_amounts = await services.get_all_income_amounts(month=month, session=session, user=user)

        return income_amounts
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/stats_by_month')
async def stats_by_month(month: Month = Depends(Month),
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user),
                         services: Services = Depends(Services)):
    try:
        expenses_amount = await services.get_all_expenses_amounts(month=month, session=session, user=user)
        income_amounts = await services.get_all_income_amounts(month=month, session=session, user=user)

        if expenses_amount == [None] and income_amounts != [None]:
            return income_amounts

        if income_amounts == [None] and expenses_amount != [None]:
            return expenses_amount

        result = income_amounts[0] - expenses_amount[0]

        return result

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
