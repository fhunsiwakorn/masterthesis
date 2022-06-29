from fastapi import APIRouter, HTTPException
from typing import List, Optional
from common.base_form import Status, StatusWithRes
from models.user import Users, User_Pydantic, UserIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError

from pydantic import BaseModel
import math

router = APIRouter(
    prefix="/user",
    tags=['User'],
    responses={404: {
        'message': "Not found"
    }

    }
)


class Login(BaseModel):
    user_name: str
    user_password: str


@router.get("/users", response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@router.get("/users/p")
async def get_users_with_pagination(page: Optional[int] = 1, per_page: Optional[int] = 50):
    if page < 1:
        pageNumber = 1
    else:
        pageNumber = page

    if per_page < 1:
        rowPerPage = 1
    elif per_page > 5000:
        rowPerPage = 5000
    else:
        rowPerPage = per_page

    totalData = await Users.all().count()
    totalpage = math.ceil(totalData / rowPerPage)
    res = await User_Pydantic.from_queryset(Users.all().offset(pageNumber-1).limit(rowPerPage))
    return StatusWithRes(status=f"Success", message=f"Show Data", page=pageNumber, per_page=rowPerPage,
                         total_data=totalData, total_page=totalpage, res_data=res)


@router.get(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: str):
    return await User_Pydantic.from_queryset_single(Users.get(user_id=user_id))


@router.post("/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.put(
    "/user/{user_id}", response_model=User_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: str, user: UserIn_Pydantic):
    await Users.filter(user_id=user_id).update(**user.dict(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(user_id=user_id))


@router.delete("/user/{user_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(user_id: str):
    deleted_count = await Users.filter(user_id=user_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"User {user_id} not found")
    return Status(status=f"Success", message=f"Deleted user {user_id}")


@router.post("/login")
async def login(item: Login):
    return await Users.get(username=item.user_name, password_hash=item.user_password)
