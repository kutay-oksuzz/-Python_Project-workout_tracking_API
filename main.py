import os
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth


APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
GENDER = "male"
WEIGHT = 84
HEIGHT = 181
AGE = 23
PASSWORD = os.environ['PASSWORD']
USERNAME = os.environ['USERNAME']
sheet_inputs = {}
auth = HTTPBasicAuth(USERNAME, PASSWORD)
Authorization = os.environ['Authorization']

exercise_endpoint = os.environ['exercise_endpoint']
sheety_endpoint = os.environ['sheety_endpoint']

HEADER = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}

parameters = {
    "query": f"{input('Tell me which exercises you did: ')}",
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,

}

now_day_month_year = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().time().strftime("%H:%M:%S")

connected = requests.post(url=exercise_endpoint, json=parameters, headers=HEADER)
connected.raise_for_status()
data = connected.json()

for exercise in data["exercises"]:
    sheet_inputs = {
        "sayfa1": {
            "date": now_day_month_year,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    response = requests.post(url=sheety_endpoint, auth=auth, json=sheet_inputs, headers=Authorization)
