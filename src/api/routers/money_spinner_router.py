from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi.exceptions import HTTPException

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.schemas import MoneySpinnerCreate, MoneySpinnerReadWithoutExpenses
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from fastapi_cache.decorator import cache

from src.api.crud_services.crud_services import CRUDmoneyspinner


router = APIRouter(
    prefix='/money_spinners',
    tags=['money_spinners']
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.get('/user_money_spinners', response_model=List[MoneySpinnerReadWithoutExpenses])
@cache(expire=60)
async def read_money_spinners_by_user(session: AsyncSession = Depends(get_async_session),
                                      user: User = Depends(current_user),
                                      crud_services: CRUDmoneyspinner = Depends(CRUDmoneyspinner)):
    try:
        money_spinners = await crud_services.get_money_spinners_by_user(session=session, user=user)

        if money_spinners == []:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return money_spinners

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/', status_code=201)
async def add_money_spinner(money_spinner: MoneySpinnerCreate,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user),
                            crud_services: CRUDmoneyspinner = Depends(CRUDmoneyspinner)):
    try:
        new_money_spinner = await crud_services.add_money_spinner(money_spinner=money_spinner,
                                                                  session=session, user=user)

        return new_money_spinner

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)


@router.delete('/{money_spinner_id}', status_code=204)
async def delete_money_spinner_by_id(money_spinner_id: int,
                                     session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user),
                                     crud_services: CRUDmoneyspinner = Depends(CRUDmoneyspinner)):
    try:
        deleted_money_spinner = await crud_services.delete_money_spinner_by_id(money_spinner_id=money_spinner_id,
                                                                               session=session,
                                                                               user=user)

        return deleted_money_spinner

    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
