from sqlalchemy import select, insert

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.expense.models import Expense
from src.api.expense.schemas import ExpenseCreate
from src.database import get_async_session

router = APIRouter(
    prefix='/expenses',
    tags=['expenses']
)


@router.get('/{expense_id}', status_code=200)
async def get_expenses(expense_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Expense).where(Expense.id == expense_id)
        query_result = await session.execute(query)
        result = query_result.scalar()
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return {
                'status': 'success',
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
async def add_expense(expense: ExpenseCreate, session: AsyncSession = Depends(get_async_session)):
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
        raise HTTPException(status_code=500, detail=
        {
            'status': 'error',
            'data': None,
            'details': None
        })