import requests
import os
import datetime as dt
from dotenv import load_dotenv

load_dotenv()
# ----------- Nutritionix API Credentials -----------
APP_ID = os.getenv('APP_ID')
API_KEY = os.getenv("API_KEY")
TOKEN = os.getenv("TOKEN")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
SHEET_ENDPOINT = os.getenv("SHEET_ENDPOINT")
SHEETY_AUTH = os.getenv("SHEETY_AUTH")

# ----------- Nutritionix API Request -----------
exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me what you did today: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
    "Content-Type": "application/json"
}

exercise_payload = {
    "query": exercise_text,
    "gender": "male",
    "weight_kg": 70,
    "height_cm": 175,
    "age": 19
}

exercise_response = requests.post(url=exercise_url, headers=headers, json=exercise_payload)
exercise_response.raise_for_status()
exercise_data = exercise_response.json()

print("📝 Nutritionix response:")
print(exercise_data)

# ----------- Sheety Setup -----------
SHEETY_URL = "https://api.sheety.co/1a698ab24274a3dcd5fec165c4692a5b/copyOfMyWorkouts/workouts"

# Optional: Sheety Basic Auth
SHEETY_HEADERS = {
    "Authorization": f"Basic {SHEETY_AUTH}"
}

# ----------- Post each exercise to Sheety -----------
now = dt.datetime.now()

for exercise in exercise_data["exercises"]:
    workout_entry = {
        "workout": {
            "date": now.strftime("%d/%m/%Y"),
            "time": now.strftime("%H:%M"),
            "exercise": exercise["name"].title(),
            "duration": round(exercise["duration_min"]),
            "calories": round(exercise["nf_calories"])
        }
    }

    sheety_response = requests.post(url=SHEETY_URL, json=workout_entry, headers=SHEETY_HEADERS)  # Add headers=SHEETY_HEADERS if needed
    print(f"📤 Sent to Sheety – Status: {sheety_response.status_code}")
    print(sheety_response.text)

