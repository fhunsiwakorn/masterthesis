from fastapi import APIRouter, HTTPException
from typing import List, Optional
from common.base_form import Status, StatusWithRes
from common.data_stable import patientRisk, genderType, agerangeType
from common.functions import get_countryName, get_provinceName
from models.patient import patient_data, patient_data_Pydantic
from models.patient import patient_data_new, patient_data_new_Pydantic, patient_data_newIn_Pydantic
from models.patient import patient_address, patient_address_Pydantic, patient_addressIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError

import math
router = APIRouter(
    prefix="/patient",
    tags=['Patient'],
    responses={404: {
        'message': "Not found"
    }

    }
)


# patient_data

# ข้อมูลผู้ป่วยเก่า


@router.get("/patient_data/p")
async def get_patient_data_with_pagination(page: Optional[int] = 1, per_page: Optional[int] = 50):
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
    totalData = await patient_data.all().count()
    totalpage = math.ceil(totalData / rowPerPage)
    res = await patient_data_Pydantic.from_queryset(patient_data.all().offset(pageNumber-1).limit(rowPerPage).order_by('-crt_date'))
    resformat = []
    for data in res:
        if data.country_code == "THA":
            nationalityType = "คนไทย"
        else:
            nationalityType = "ชาวต่างชาติ"
        lists = {'ptd_id': data.ptd_id, "gender": genderType[data.gd_id-1]['gd_name'],
                 'ptd_age': data.ptd_age, 'arType': agerangeType[int(data.ar_id)-1]['ar_name'], 'nationality': get_countryName(data.country_code),
                 'nationalityType': nationalityType, 'province': get_provinceName(data.province_code), 'patient_risk': patientRisk[int(data.ptr_id)-1]['ptr_name'],
                 'crt_date': str(data.crt_date), 'upd_date': str(data.upd_date)}
        resformat.append(lists)

    return StatusWithRes(status=f"Success", message=f"Show Data", page=pageNumber, per_page=rowPerPage,
                         total_data=totalData, total_page=totalpage, res_data=resformat)

# ข้อมูลผู้ป่วยเก่าล่าสุด


@router.get("/patient_data/{ptd_id}", response_model=patient_data_Pydantic)
async def get_patient_data_id(ptd_id: int):
    return await patient_data_Pydantic.from_queryset_single(patient_data.get(ptd_id=ptd_id))


# ข้อมูลผู้ป่วยใหม่ล่าสุด
@router.get("/patient_data_new/last", response_model=patient_data_new_Pydantic)
async def get_patient_data_last():
    lastid = await patient_data_new_Pydantic.from_queryset(patient_data_new.all().order_by("-ptd_id").limit(1))
    return lastid[0]

# เพิ่มข้อมูลผู้ป่วยใหม่


@router.post("/patient_data_new", response_model=patient_data_new_Pydantic)
async def create_patient_data(item: patient_data_newIn_Pydantic):
    item_obj = await patient_data_new.create(**item.dict(exclude_unset=True))
    return await patient_data_newIn_Pydantic.from_tortoise_orm(item_obj)

# ข้อมูลผู้ป่วยใหม่


@router.get("/patient_data_new/p")
async def get_patient_data_new_with_pagination(page: Optional[int] = 1, per_page: Optional[int] = 50):
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
    totalData = await patient_data_new.all().count()
    totalpage = math.ceil(totalData / rowPerPage)
    res = await patient_data_new_Pydantic.from_queryset(patient_data_new.all().offset(pageNumber-1).limit(rowPerPage).order_by('-crt_date'))
    resformat = []
    for data in res:
        if data.country_code == "THA":
            nationalityType = "คนไทย"
        else:
            nationalityType = "ชาวต่างชาติ"
        lists = {'ptd_id': data.ptd_id, "gender": genderType[data.gd_id-1]['gd_name'],
                 'ptd_age': data.ptd_age, 'arType': agerangeType[int(data.ar_id)-1]['ar_name'], 'nationality': get_countryName(data.country_code),
                 'nationalityType': nationalityType, 'province': get_provinceName(data.province_code), 'patient_risk': patientRisk[int(data.ptr_id)-1]['ptr_name'],
                 'crt_date': str(data.crt_date), 'upd_date': str(data.upd_date)
                 }
        resformat.append(lists)

    return StatusWithRes(status=f"Success", message=f"Show Data", page=pageNumber, per_page=rowPerPage,
                         total_data=totalData, total_page=totalpage, res_data=resformat)

# ดึงข้อมูลผู้ป่วยใหม่ด้วย id


@router.get("/patient_data_new/{ptd_id}", response_model=patient_data_new_Pydantic)
async def get_patient_data_id(ptd_id: int):
    return await patient_data_new_Pydantic.from_queryset_single(patient_data_new.get(ptd_id=ptd_id))

# แก้ไขข้อมูลผู้ป่วยใหม่


@router.put(
    "/patient_data_new/{ptd_id}", response_model=patient_data_new_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_patient_data(ptd_id: int, item: patient_data_newIn_Pydantic):
    await patient_data_new.filter(ptd_id=ptd_id).update(**item.dict(exclude_unset=True))
    return await patient_data_new_Pydantic.from_queryset_single(patient_data_new.get(ptd_id=ptd_id))

# ลบข้อมูลผู้ป่วยใหม่


@router.delete("/patient_data_new/{ptd_id}", response_model=Status, responses={404: {"model": HTTPNotFoundError}})
async def delete_user(ptd_id: int):
    deleted_count = await patient_data_new.filter(ptd_id=ptd_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"ID {ptd_id} not found")
    return Status(status=f"Success", message=f"Deleted ID {ptd_id}")

# เพิ่มที่อยู่ผู้ป่วย


@router.post("/patient_address", response_model=patient_address_Pydantic)
async def create_patient_address(item: patient_addressIn_Pydantic):
    item_obj = await patient_address.create(**item.dict(exclude_unset=True))
    return await patient_addressIn_Pydantic.from_tortoise_orm(item_obj)

# แก้ไขที่อยู่ผู้ป่วย


@router.put(
    "/patient_address/{ptd_id}", response_model=patient_address_Pydantic, responses={404: {"model": HTTPNotFoundError}}
)
async def update_patient_data(ptd_id: int, item: patient_addressIn_Pydantic):
    await patient_address.filter(ptd_id=ptd_id).update(**item.dict(exclude_unset=True))
    return await patient_address_Pydantic.from_queryset_single(patient_address.get(ptd_id=ptd_id))

# ดึงข้อมูลรายละเอียดผู้ป่วยด้วย id


@router.get("/patient_address/{ptd_id}", response_model=patient_address_Pydantic)
async def get_patient_address_id(ptd_id: int):
    return await patient_address_Pydantic.from_queryset_single(patient_address.get(ptd_id=ptd_id))
