from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.schemas import ExpenseCreate, MoneySpinnerReadWithExpenses
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from src.api.crud_services.crud_services import CRUDexpense


router = APIRouter(
    prefix='/expenses',
    tags=['expenses']
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.get('/expenses', status_code=200, response_model=List[MoneySpinnerReadWithExpenses])
async def read_expenses_by_user(session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(current_user),
                                crud_services: CRUDexpense = Depends(CRUDexpense)):
    result = await crud_services.get_expenses_by_user(session=session, user=user)

    if result == []:
        raise HTTPException(status_code=404, detail='You have no expenses')

    return result


@router.post('/', status_code=201)
async def add_expense(expense: ExpenseCreate, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user),
                      crud_services: CRUDexpense = Depends(CRUDexpense)):
    try:
        new_expense = await crud_services.add_expense(expense=expense, session=session, user=user)

        return new_expense
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/', status_code=204)
async def delete_expense_by_id(expense_id: int,
                               session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user),
                               crud_services: CRUDexpense = Depends(CRUDexpense)):
    try:
        deleted_expense = await crud_services.delete_expense_by_id(expense_id=expense_id,
                                                                   session=session, user=user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)