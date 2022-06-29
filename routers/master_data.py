from fastapi import APIRouter
from common.data_stable import agerangeType, patientRisk, patientType

router = APIRouter(
    prefix="/master_data",
    tags=['MasterData'],
    responses={404: {
        'message': "Not found"
    }

    }
)


@router.get("/agerange")
def read_agerange():
    return agerangeType


@router.get("/patient_risk")
def read_patient_risk():
    return patientRisk


@router.get("/patient_type")
def read_patient_type():
    return patientType
