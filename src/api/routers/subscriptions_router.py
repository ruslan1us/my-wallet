from typing import List

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.expense.schemas import SubscriptionRead, SubscriptionCreate
from src.database import get_async_session

from fastapi_users import FastAPIUsers

from fastapi_cache.decorator import cache

from src.api.crud_services.crud_services import CRUDSubscription

router = APIRouter(
    prefix='/expenses/subscriptions',
    tags=['expenses/subscriptions']
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()


@router.get('/subscriptions', status_code=200, response_model=List[SubscriptionRead])
async def read_subscriptions_by_user(session: AsyncSession = Depends(get_async_session),
                                     user: User = Depends(current_user),
                                     crud_services: CRUDSubscription = Depends(CRUDSubscription)):
    result = await crud_services.get_all_subscriptions(session=session, user=user)

    if result == []:
        raise HTTPException(status_code=404, detail='You have no subscriptions')

    return result


@router.post('/', status_code=201)
async def add_subscription(sub: SubscriptionCreate, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user),
                           crud_services: CRUDSubscription = Depends(CRUDSubscription)):
    try:
        new_subscription = await crud_services.add_subscription(sub=sub, session=session, user=user)

        return new_subscription
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete('/{sub_id}', status_code=204)
async def delete_subscription_by_id(sub_id: int,
                                    session: AsyncSession = Depends(get_async_session),
                                    user: User = Depends(current_user),
                                    crud_services: CRUDSubscription = Depends(CRUDSubscription)):
    try:
        deleted_subscription = await crud_services.delete_subscription_by_id(sub_id=sub_id,
                                                                             session=session, user=user)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
