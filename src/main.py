import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.auth.schemas import UserRead, UserCreate

from fastapi_users import FastAPIUsers

from src.api.routers.tip_router import router as tip_router
from src.api.routers.money_spinner_router import router as money_spinner_router
from src.api.routers.expense_router import router as expense_router
from src.api.routers.income_router import router as income_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # await create_tables()
    print('Starting...')
    yield
    # await delete_tables()
    print('Off...')

app = FastAPI(
    title='Financial literacy(My Wallet)',
    lifespan=lifespan
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(expense_router)

app.include_router(money_spinner_router)

app.include_router(income_router)

app.include_router(tip_router)

if __name__ == "__main__":
    uvicorn.run(app=app)
