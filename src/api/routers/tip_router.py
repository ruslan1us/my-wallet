from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.income.schemas import TipRead, TipCreate
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from fastapi_cache.decorator import cache

from src.api.crud_services.crud_services import CRUDtip

router = APIRouter(
    prefix='/income/tip',
    tags=['income/tip']
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.post('/', status_code=201)
async def add_tip(tip: TipCreate,
                  session: AsyncSession = Depends(get_async_session),
                  user: User = Depends(current_user),
                  crud_services: CRUDtip = Depends(CRUDtip)):
    try:
        new_tip = await crud_services.add_tip(tip=tip, session=session, user=user)

        return {'status': 'success', 'data': new_tip, 'message': 'Tip is successfully added'}

    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.get('/all_tip', response_model=List[TipRead])
@cache(expire=60)
async def read_all_tips(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user),
                        crud_services: CRUDtip = Depends(CRUDtip)):
    tips = await crud_services.get_all_tips(session=session, user=user)

    if tips == []:
        raise HTTPException(status_code=404, detail='You have no tips')

    return {'status': 'success', 'data': tips}


@router.delete('/{tip_id}', status_code=204)
async def delete_tip_by_id(tip_id: int,
                           session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user),
                           crud_services: CRUDtip = Depends(CRUDtip)):
    try:
        deleted_tip = await crud_services.delete_tip_by_id(tip_id=tip_id, session=session,
                                                           user=user)

        return {'status': 'success', 'data': deleted_tip, 'message': 'Tip is successfully deleted'}
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)