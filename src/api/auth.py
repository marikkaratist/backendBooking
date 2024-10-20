from fastapi import APIRouter, Body, HTTPException
from passlib.context import CryptContext
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аунтентификация"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        user_repo = UsersRepository(session)
        if await user_repo.user_exists(data.email):
            raise HTTPException(status_code=400, detail="Email already exists")

        await user_repo.add(new_user_data)
        await session.commit()
    return {"status": 201}
