from pydantic import BaseModel


class Status(BaseModel):
    status: str
    message: str


class StatusWithRes(BaseModel):
    status: str
    message: str
    page: int
    per_page: int
    total_data: int
    total_page: int
    res_data: list


class Predict(BaseModel):
    gender: int
    age_range: int
    nationality_type: int
    risk: int
    province: int
