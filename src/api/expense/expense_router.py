from typing import List

from sqlalchemy import select

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.models import Expense
from src.api.expense.models import MoneySpinnerTable
from src.api.expense.schemas import ExpenseCreate, MoneySpinnerReadWithExpenses
from src.database import get_async_session

from fastapi_users import FastAPIUsers


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
async def get_expenses_by_user(session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user)):
    query = (select(MoneySpinnerTable).options(joinedload(MoneySpinnerTable.expenses))
                                      .where(MoneySpinnerTable.owner_id == user.id))
    query_result = await session.execute(query)
    result = query_result.scalars().unique().all()

    if result == []:
        raise HTTPException(status_code=404, detail='You have no expenses')
    return result


@router.post('/', status_code=201)
async def add_expense(expense: ExpenseCreate, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    try:
        new_expense = Expense(**expense.model_dump(), owner_id=user.id)

        session.add(new_expense)
        await session.commit()
        await session.refresh(new_expense)

        return {
            'status': 'success',
            'data': f'added {expense}',
            'details': None
        }
    except:
        raise HTTPException(status_code=400, detail=
        {
            'status': 'Bad request',
            'data': None,
            'details': None
        })


@router.delete('/', status_code=204)
async def delete_expense_by_id(expense_id: int,
                               session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(current_user)):
    expense = await session.get(Expense, expense_id)

    if not expense:
        raise HTTPException(status_code=404, detail=f'No expense with this id: {expense_id}')

    await session.delete(expense)
    await session.commit()
