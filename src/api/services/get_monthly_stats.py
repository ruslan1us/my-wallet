from fastapi_users import FastAPIUsers
from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.models import Expense
from src.api.expense.schemas import ExpenseRead
from src.database import get_async_session

from pydantic import Field, BaseModel

from typing import List


router = APIRouter(
    prefix='/services',
    tags=['services']
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


class Month(BaseModel):
    month: int = Field(None, ge=1, le=12)


@router.get('/monthly_expenses_stats', response_model=List[ExpenseRead])
async def get_monthly_expenses_stats(month: Month = Depends(Month),
                                     session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user)):
    month = month.model_dump()
    expense_query = select(Expense).where(month.get('month') == func.date_part('month', Expense.expensed_at),
                                          Expense.owner_id == user.id)

    query_result = await session.execute(expense_query)
    result = query_result.scalars().all()

    if result == []:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='You have no expenses this month')

    return result
