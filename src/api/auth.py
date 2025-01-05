from fastapi import APIRouter, Body, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    UserAlreadyExistsException,
    UserEmailAlreadyExistsHTTPException,
    EmailNotRegisteredException,
    EmailNotRegisteredHTTPException,
    IncorrectPasswordException,
    IncorrectPasswordHTTPException,
)
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аунтентификация"])


@router.post("/register")
async def register(
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Admin",
                "value": {"email": "admin_example@mgmail.com", "password": "PasSsw0rD"},
            },
            "2": {
                "summary": "User",
                "value": {"email": "user_example@mgmail.com", "password": "91sdjer99"},
            },
        }
    ),
):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException

    return {"status": 200}


@router.post("/login")
async def login_user(
    response: Response,
    db: DBDep,
    data: UserRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Admin",
                "value": {"email": "admin_example@mgmail.com", "password": "PasSsw0rD"},
            },
            "2": {
                "summary": "User",
                "value": {"email": "user_example@mgmail.com", "password": "91sdjer99"},
            },
        }
    ),
):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)

    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me", summary="🧑‍💻 Мой профиль")
async def me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)
