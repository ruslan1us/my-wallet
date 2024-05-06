from typing import List

from fastapi import APIRouter, Depends, status, BackgroundTasks
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.crud_services.crud_monthly import CRUDyear
from src.api.expense.schemas import ExpenseRead
from src.api.income.schemas import TipRead, SalaryRead
from src.api.services.models import Month, Day, Year
from src.api.services.send_mail import send_email_async, send_email_background
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from src.api.services.statistics_services import Services

router = APIRouter(
    prefix='/services',
    tags=['services']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.get('/all_expenses_amounts_by_day')
async def all_expenses_amounts_by_day(day: Day = Depends(Day),
                                      month: Month = Depends(Month),
                                      session: AsyncSession = Depends(get_async_session),
                                      user: User = Depends(current_user),
                                      services: Services = Depends(Services)):
    try:
        expenses_amount = await services.get_all_expenses_amounts_by_day(day=day, month=month,
                                                                         session=session, user=user)

        if expenses_amount == [None]:
            raise Exception

        return expenses_amount
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/year_expense', response_model=List[ExpenseRead])
async def get_year_expense(year: Year = Depends(Year),
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user),
                           crud_services: CRUDyear = Depends(CRUDyear)):
    try:
        expenses = await crud_services.get_year_expense(year=year, session=session, user=user)

        if expenses == []:
            raise Exception

        return expenses

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/year_salary', response_model=List[SalaryRead])
async def get_year_salary(year: Year = Depends(Year),
                          session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user),
                          crud_services: CRUDyear = Depends(CRUDyear)):
    try:
        salary = await crud_services.get_year_salary(year=year, session=session, user=user)

        if salary == []:
            raise Exception

        return salary

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/year_tip', response_model=List[TipRead])
async def get_year_tip(year: Year = Depends(Year),
                       session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user),
                       crud_services: CRUDyear = Depends(CRUDyear)):
    try:
        tip = await crud_services.get_year_tip(year=year, session=session, user=user)

        if tip == []:
            raise Exception

        return tip

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get('/biggest_expense')
async def get_the_biggest_expense(session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(current_user),
                                  services: Services = Depends(Services)):

    expense = await services.get_the_biggest_expense(session=session, user=user)

    return expense


@router.get('/send_mail_month_report')
async def send_mail_month_report(background_tasks: BackgroundTasks,
                                 session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(current_user),
                                 services: Services = Depends(Services)):
    expense = await services.get_the_biggest_expense(session=session, user=user)

    if expense == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    expense_dict_money_spinner = expense[0][0].__dict__
    expense_dict_expense = expense[1][0].__dict__

    send_email_background(background_tasks, {
                          'subject': 'Month Report',
                          'email_to': f'{user.email}',
                          'body': {'money_spinner': f'{expense_dict_money_spinner.get('name')}',
                                   'amount': f'{expense_dict_expense.get('amount')}',
                                   'date': f'{expense_dict_expense.get('expensed_at')}',
                                   'name': f'{user.username}'}
                          })
