from sqlalchemy import select, insert

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.models import Expense
from src.api.expense.schemas import ExpenseCreate, ExpenseUpdate, ExpenseRead
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


@router.get('/{expense_id}', status_code=200)
async def get_expense_by_id(expense_id: int, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        query = select(Expense).where(Expense.id == expense_id)
        query_result = await session.execute(query)
        result = query_result.scalar()

        if result is None:
            raise Exception

        return {
                'status': 'OK',
                'data': result,
                'details': None
        }
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=
        {
            'status': 'NOT_FOUND',
            'data': None,
            'details': f'No expense with id: {expense_id}'
        })


@router.post('/', status_code=201)
async def add_expense(expense: ExpenseCreate, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    try:
        new_expense = Expense(**expense.model_dump())

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