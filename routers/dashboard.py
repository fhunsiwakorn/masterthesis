from fastapi import APIRouter
from typing import Optional
from models.patient import patient_data
from common.base_form import Predict
from common.data_stable import patientType
from enum import Enum
import json
import requests
router = APIRouter(
    prefix="/dashboard",
    tags=['Dashboard'],
    responses={404: {
        'message': "Not found"
    }

    }
)


class DatePart(Enum):
    year = "YEAR"
    quarter = "QUARTER"
    month = "MONTH"
    week = "WEEK"
    day = "DAY"
    hour = "HOUR"
    minute = "MINUTE"
    second = "SECOND"
    microsecond = "MICROSECOND"


@router.get("/patient/month")
async def get_dashboard_month(year: Optional[int] = 2021):
    x = range(12)
    result = []
    for n in x:
        # print(n+1)
        month = n+1
        list_months = await patient_data.filter(crt_date__month=month, crt_date__year=year).count()
        result.append(list_months)
    return {'count': result}


@router.get("/patient/total/province")
async def get_dashboard_total_province():
    # for i in range(10, 8):
    #     bkk = await patient_data.filter(province_code=10).count()
    url = 'http://localhost:1112/province'
    provinceList = json.loads(requests.get(url).text)
    totalList = []
    for r in provinceList:
        province_code = r['province_code']
        hc_key = r['hc_key']
        total = await patient_data.filter(province_code=province_code).count()
        merg = [str(hc_key), total]
        totalList.append(merg)

    return {'data': totalList}


@router.post("/check_true")
async def check_true(item: Predict):
    gender = int(item.gender)
    age_range = int(item.age_range)
    nationality_type = int(item.nationality_type)
    risk = int(item.risk)
    province = int(item.province)
    i = 0
    newFormat = []
    for pt in patientType:
        i += 1
        total = await patient_data.filter(gd_id=gender, ar_id=age_range, nt_id=nationality_type, ptr_id=risk, province_code=province, ptt_id=i).count()
        res = {'ptt_name': pt['ptt_name'], 'total': total}
        newFormat.append(res)
    return newFormat
