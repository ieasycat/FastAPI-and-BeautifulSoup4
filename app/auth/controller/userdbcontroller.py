from app.auth.models.models import UserSchema, UserLoginSchema
from app.auth.models.userdb import User, User_Pydantic
from passlib.hash import bcrypt
from config.config import CONFIG
import jwt


class UserDbController:
    @staticmethod
    async def authenticate_user(user):
        user_obj = await User.get_or_none(email=user.email)
        if not user_obj:
            return "Email doesn't exist"
        if not user_obj.verify_password(user.password):
            return "Wrong password"
        return user_obj

    @staticmethod
    async def create_user(user: UserSchema) -> User:
        new_user = await User.create(email=user.email, password_hash=bcrypt.hash(user.password))
        await new_user.save()
        return new_user

    @staticmethod
    async def generate_token(user: UserLoginSchema) -> str:
        user_obj = await User_Pydantic.from_tortoise_orm(user)
        return jwt.encode(user_obj.dict(), CONFIG.JWT_SECRET_KEY, algorithm=CONFIG.JWT_ALGORITHM)
