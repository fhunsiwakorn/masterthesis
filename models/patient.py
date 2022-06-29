
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from common.functions import dateTimeNow

present_time = dateTimeNow()


class patient_data(models.Model):
    ptd_id = fields.IntField(pk=True, default=0)
    gd_id = fields.IntField(default=0, blank=False)
    ptd_age = fields.IntField(default=0, blank=False)
    ar_id = fields.IntField(default=0, blank=False)
    nt_id = fields.IntField(default=0, blank=False)
    country_code = fields.CharField(max_length=3, blank=True)
    ptr_id = fields.IntField(default=0, blank=False)
    province_code = fields.IntField(default=0, blank=False)
    ptt_id = fields.IntField(default=0, blank=False)
    crt_date = fields.DatetimeField(blank=True, null=True)
    upd_date = fields.DatetimeField(default=present_time, auto_now=True)

    def __str__(self):
        return self.province_code


patient_data_Pydantic = pydantic_model_creator(
    patient_data, name="patient_data")
patient_dataIn_Pydantic = pydantic_model_creator(
    patient_data, name="patient_dataIn", exclude_readonly=True)


class patient_data_new(models.Model):
    ptd_id = fields.IntField(pk=True, default=0)
    gd_id = fields.IntField(default=0, blank=False)
    ptd_age = fields.IntField(default=0, blank=False)
    ar_id = fields.IntField(default=0, blank=False)
    nt_id = fields.IntField(default=0, blank=False)
    country_code = fields.CharField(max_length=3, blank=True)
    ptr_id = fields.IntField(default=0, blank=False)
    province_code = fields.IntField(default=0, blank=False)
    ptt_id = fields.IntField(default=0, blank=False)
    crt_date = fields.DatetimeField(blank=True, null=True)
    upd_date = fields.DatetimeField(default=present_time, auto_now=True)

    def __str__(self):
        return self.province_code


patient_data_new_Pydantic = pydantic_model_creator(
    patient_data_new, name="patient_data_new")
patient_data_newIn_Pydantic = pydantic_model_creator(
    patient_data_new, name="patient_data_newIn", exclude_readonly=True)


class patient_address(models.Model):
    pta_id = fields.IntField(pk=True, default=0)
    pta_idcard = fields.CharField(max_length=128, blank=False)
    pta_firstname = fields.CharField(max_length=254, blank=False)
    pta_lastname = fields.CharField(max_length=254, blank=False)
    pta_address_number = fields.CharField(max_length=254, null=True)
    pta_email = fields.CharField(max_length=254, null=True)
    pta_phone = fields.CharField(max_length=254, null=True)
    pta_img = fields.CharField(max_length=254, null=True)
    province_code = fields.IntField(default=0, blank=False)
    amphur_code = fields.IntField(default=0, blank=False)
    district_code = fields.IntField(default=0, blank=False)
    zipcode = fields.IntField(default=0, blank=False)
    ptd_id = fields.IntField(default=0, blank=False)
    crt_date = fields.DatetimeField(blank=True, null=True)
    upd_date = fields.DatetimeField(default=present_time, auto_now=True)

    def __str__(self):
        return self.pta_firstname


patient_address_Pydantic = pydantic_model_creator(
    patient_address, name="patient_address")
patient_addressIn_Pydantic = pydantic_model_creator(
    patient_address, name="patient_addressIn", exclude_readonly=True)
