
import uuid
import json
import requests
from datetime import datetime, timezone, timedelta


def generateId():
    return uuid.uuid4().hex[:24]


def dateTimeNow():
    # Time zone in Thailand UTC+7
    tz = timezone(timedelta(hours=7))
    # Create a date object with given timezone
    date = datetime.now(tz=tz)
    # Display time
    # print(date.isoformat(sep = " "))
    dateTimeNow = date.isoformat(sep=" ")
    return dateTimeNow


def get_countryName(country_code):
    url = "https://masterdata.thaionzon.com/country_alpha3/" + \
        str(country_code)

    resp = json.loads(requests.get(url).text)
    return str(resp['country_name_th']).encode('utf-8')


def get_provinceName(province_code):
    url = "https://masterdata.thaionzon.com/province/" + \
        str(province_code)

    resp = json.loads(requests.get(url).text)
    return str(resp['province_name']).encode('utf-8')


# print(get_countryName('THA'))
# print(get_provinceName('10'))
# print(dateTimeNow())
