from app.auth.models.userdb import User, User_Pydantic
from fastapi import APIRouter
from app.auth.controller.userdbcontroller import UserDbController
from app.auth.models.models import UserSchema, UserLoginSchema
from app.auth.apiexception import api_exception

auth_router = APIRouter()


@auth_router.post('/register')
async def create_user(user: UserSchema):
    user_check = await User.get_or_none(email=user.email)
    if user_check:
        raise api_exception(status_code=401, detail='User already registered')
    new_user = await UserDbController.create_user(user=user)
    return await User_Pydantic.from_tortoise_orm(new_user)


@auth_router.post('/token')
async def generate_token(user: UserLoginSchema):
    check = await UserDbController.authenticate_user(user=user)
    if isinstance(check, str):
        raise api_exception(status_code=401, detail=check)
    token = await UserDbController.generate_token(user=check)
    return {'access_token': token, 'token_type': 'bearer'}

