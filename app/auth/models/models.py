from pydantic.fields import Field
from pydantic.main import BaseModel
from pydantic.networks import EmailStr


class UserSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "userpassword"
            }
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "userpassword"
            }
        }
