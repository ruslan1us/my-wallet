from fastapi import APIRouter

from src.api.auth.auth import auth_backend
from src.api.auth.manager import get_user_manager
from src.api.auth.models import User
from src.api.auth.schemas import UserRead, UserCreate

from fastapi_users import FastAPIUsers


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

jwt_router = APIRouter(
    prefix="/auth/jwt",
    tags=["auth"]
)

jwt_router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_verify_router(UserRead))
