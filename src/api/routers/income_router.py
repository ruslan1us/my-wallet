from typing import List

from fastapi import APIRouter, Depends, status

from fastapi_users import FastAPIUsers

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.exceptions import HTTPException

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.income.schemas import SalaryCreate, SalaryRead
from src.database import get_async_session

from fastapi_cache.decorator import cache

from src.api.crud_services.crud_services import CRUDincome

router = APIRouter(
    prefix='/income',
    tags=['income']
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.post('/', status_code=201)
async def add_salary(salary: SalaryCreate,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user),
                     crud_services: CRUDincome = Depends(CRUDincome)):
    try:
        new_salary = await crud_services.add_salary(salary=salary, session=session, user=user)

        return {'status': 'success', 'data': new_salary, 'message': 'Salary is successfully added'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Bad request information')


@router.get('/all_salary')      # response_model=List[SalaryRead]
@cache(expire=60)
async def read_all_salary(session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user),
                          crud_services: CRUDincome = Depends(CRUDincome)):
    salaries = await crud_services.get_all_salary(session=session, user=user)

    if salaries == []:
        raise HTTPException(status_code=404, detail='You have no salaries')

    return {'status': 'success', 'data': salaries}


@router.delete('/{salary_id}', status_code=204)
async def delete_salary_by_id(salary_id: int,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user),
                              crud_services: CRUDincome = Depends(CRUDincome)):
    try:
        deleted_salary = await crud_services.delete_salary_by_id(salary_id=salary_id, session=session,
                                                                 user=user)

        return {'status': 'success', 'data': deleted_salary, 'message': 'Salary is successfully deleted'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
