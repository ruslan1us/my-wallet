from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.services.models import Month
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


@router.get('/all_expenses_amounts')
async def all_expenses_amounts(month: Month = Depends(Month),
                               session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user),
                               services: Services = Depends(Services)):
    try:
        expenses_amount = await services.get_all_expenses_amounts(month=month, session=session, user=user)

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