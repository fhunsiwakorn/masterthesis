from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from common.functions import dateTimeNow

# https://tortoise.github.io/examples/fastapi.html
present_time = dateTimeNow()


class Users(models.Model):
    user_id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=20, unique=True)
    first_name = fields.CharField(max_length=128, null=True)
    last_name = fields.CharField(max_length=128, null=True)
    password_hash = fields.CharField(max_length=128, null=True)
    crt_date = fields.DatetimeField(blank=True, null=True)
    upd_date = fields.DatetimeField(default=present_time)
    active = fields.IntField(default=0, blank=False)
    cancelled = fields.IntField(default=1, blank=False)

    def __str__(self):
        return self.username


User_Pydantic = pydantic_model_creator(Users, name="User")
UserIn_Pydantic = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True)
