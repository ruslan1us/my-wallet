from celery import Celery
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.api.auth.models import User

celery = Celery('tasks', broker='redis://localhost:6379')

async def get_all_users(session: AsyncSession):
    query = select(User)

    result = await session.execute(query)

    users = result.scalars().all()

    return users

