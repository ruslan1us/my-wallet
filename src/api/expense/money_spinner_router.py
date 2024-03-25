from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi.exceptions import HTTPException

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.schemas import MoneySpinnerCreate, MoneySpinnerReadWithoutExpenses
from src.database import get_async_session

from src.api.expense.models import MoneySpinnerTable

from fastapi_users import FastAPIUsers

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
async def get_money_spinners_by_user(session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    query = select(MoneySpinnerTable).where(MoneySpinnerTable.owner_id == user.id)
    query_result = await session.execute(query)
    result = query_result.scalars().all()

    if result == []:
        raise HTTPException(status_code=404, detail='You have no money-spinners')
    return result


@router.post('/', status_code=201)
async def add_money_spinner(money_spinner: MoneySpinnerCreate,
                            session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(current_user)):
    try:
        new_money_spinner = MoneySpinnerTable(**money_spinner.model_dump(), owner_id=user.id)
        session.add(new_money_spinner)
        await session.commit()
        await session.refresh(new_money_spinner)

        return {
            'status': 'Created',
            'data': f'{money_spinner}',
            'details': 'Money-spinner successfully added'
        }
    except IntegrityError:
        raise HTTPException(status_code=409, detail=
        {
            'status': 'Money-spinner already exist',
            'data': None,
            'details': None
        })


@router.delete('/', status_code=204)
async def delete_money_spinner_by_id(money_spinner_id: int,
                                     session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    money_spinner = await session.get(MoneySpinnerTable, money_spinner_id)

    if not money_spinner:
        raise HTTPException(status_code=404, detail=f'No expense with this id: {money_spinner_id}')

    await session.delete(money_spinner)
    await session.commit()
