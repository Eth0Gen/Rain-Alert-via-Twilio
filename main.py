# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

import os
import requests
from twilio.rest import Client


OWM_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
MY_LAT = 22.944101
MY_LONG = 88.433502
API_KEY = os.environ.get("OWM_API_KEY")
ACCOUNT_SID = os.environ.get("OWM_ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
SEND_TO_PHONE_NUMBER = os.environ.get("TO_PHONE_NUMBER")

parameter = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(url=OWM_API_ENDPOINT, params=parameter)
response.raise_for_status()
# stat_code = response.status_code
weather_data = response.json()

weather_forecast_list = weather_data["list"]

will_rain = False

for hour_data in weather_forecast_list:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        to=SEND_TO_PHONE_NUMBER,
        from_=TWILIO_PHONE_NUMBER,
        body="It's going to rain today. Remember to bring an Umbrella ☔!"
    )
    print(message.status)

