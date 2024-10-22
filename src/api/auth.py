from fastapi import APIRouter, Body, HTTPException, Response
from starlette.responses import RedirectResponse

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аунтентификация"])


@router.post("/register")
async def register(data: UserRequestAdd = Body(openapi_examples={
    "1": {
        "summary": "Admin", "value": {
            "email": "admin_example@mgmail.com",
            "password": "PasSsw0rD"
        }
    },
    "2": {
        "summary": "User", "value": {
            "email": "user_example@mgmail.com",
            "password": "91sdjer99"
        }
    }
})
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": 201}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)

        if user is None:
            raise HTTPException(status_code=401, detail="Пользователя с таким email не существует")

        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверный пароль")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return {"access_token": access_token}


@router.get("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get("/me")
async def me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user
