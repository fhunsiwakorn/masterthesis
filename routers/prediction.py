from fastapi import APIRouter
from common.base_form import Predict
from common.data_stable import patientType
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json
import random
import pickle
router = APIRouter(
    prefix="/predict",
    tags=['Predict'],
    responses={404: {
        'message': "Not found"
    }

    }
)

f = open('dataset/covid_v2.json')
data = json.load(f)
dataset = data['RECORDS']


@router.post("/startpredict")
async def predict(item: Predict):
    # ทำการ Load โมเดลที่เก็บไว้
    model = pickle.load(open("RFMODEL.pkcls", "rb"))
    gender = int(item.gender)
    age_range = int(item.age_range)
    nationality_type = int(item.nationality_type)
    risk = int(item.risk)
    province = int(item.province)
    # ข้อมูลผู้ป่วยใหม่
    new_data = [[gender, age_range, nationality_type, risk, province]]
    #result ['4']
    # ทำนาย

    result = model.predict(new_data)
    rsmath = patientType[int(result[0]) - 1]['ptt_name']
    return {'result': str(rsmath), 'type': int(result[0])}


@router.get("/accuracy")
async def accuracy():
    merg_feature = []
    merg_label = []

    i = 0
    totaldata = len(dataset)
    random.shuffle(dataset)
    for x in dataset:
        i += 1
        if i == 100000:
            break

        feature = [x['gender'], x['age_range'],
                   x['nationality_type'], x['risk'], x['province']]
        label = str(x['patient_type'])
        merg_feature.append(feature)
        merg_label.append(label)
    X = merg_feature
    y = merg_label

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=15)
    forest_clf = RandomForestClassifier(warm_start=True).fit(X_train, y_train)
    y_pred_test = forest_clf.predict(X_test)
    r = accuracy_score(y_test, y_pred_test)
    TrainSetAccuracy = forest_clf.score(X_train, y_train)
    TestSetAccuracy = forest_clf.score(X_test, y_test)
    return {'TrainSetAccuracy': TrainSetAccuracy, 'TestSetAccuracy': TestSetAccuracy, 'Accuracy': r, 'totalData': totaldata}
