from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt


class User(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=128, null=False)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
