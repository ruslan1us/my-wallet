from typing import List

from fastapi import APIRouter, Depends

from fastapi_users import FastAPIUsers

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from fastapi.exceptions import HTTPException

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.income.models import Salary
from src.api.income.schemas import SalaryCreate, SalaryRead
from src.database import get_async_session

router = APIRouter(
    prefix='/income',
    tags=['income']
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.post('/')
async def add_salary(salary: SalaryCreate,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    new_salary = Salary(**salary.model_dump(), owner_id=user.id)

    session.add(new_salary)
    await session.commit()
    await session.refresh(new_salary)

    raise HTTPException(status_code=201, detail=f'Created salary: {salary}')


@router.get('/all_salary', response_model=List[SalaryRead])
async def get_all_salary(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_user)):
    query = select(Salary).where(Salary.owner_id == user.id)
    query_result = await session.execute(query)
    result = query_result.scalars().all()

    if result == []:
        raise HTTPException(status_code=404, detail='You have no salary')
    return result


@router.delete('/', status_code=204)
async def delete_salary_by_id(salary_id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    salary = await session.get(Salary, salary_id)

    if not salary:
        raise HTTPException(status_code=404, detail=f'No expense with this id: {salary_id}')

    await session.delete(salary)
    await session.commit()
