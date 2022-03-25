import json
import requests
import os
import streamlit as st
from dotenv import load_dotenv

# docs for 30 day climate forcast
# https://openweathermap.org/api/forecast30#resp-year
BASE_URL = "https://pro.openweathermap.org/data/2.5/forecast/climate"


def get_weather_pred(loc: dict, local=True):

    if local == True:
        load_dotenv()
        WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
    else:
        WEATHER_API_KEY = st.secrets["WEATHER_API_KEY"]

    zip_code = loc["zip_code"]
    cnt_code = loc["cnt_code"].replace(" ", "")

    URL = BASE_URL + f"?zip={zip_code},{cnt_code}&appid={WEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(
            url=URL,
            headers={
                "Content-Type": "application/json",
            },
        )
        pred = response.json()

    except Exception as e:
        st.write(e)

    return pred


def get_part_of_day(x: int):
    if (x > 4) and (x <= 12):
        return "morn"
    elif (x > 12) and (x <= 17):
        return "day"
    elif (x > 17) and (x <= 21):
        return "eve"
    elif (x > 21) or (x <= 4):
        return "night"


def weather_info(w_dict: dict, day_from: int, hour: int):

    """Returns necessary weather info in a dict"""

    if day_from > 30:
        return None

    part_of_day = get_part_of_day(hour)

    coords_dict = w_dict["city"]["coord"]

    info_list = w_dict["list"][day_from]

    weather_dict = {
        "lat": coords_dict["lat"],
        "lon": coords_dict["lon"],
        "wind_speed": info_list["speed"],
        "wind_dir": info_list["deg"],
        "temp": info_list["temp"],
        "air_temp": info_list["temp"][part_of_day],
        "feels_like": info_list["feels_like"],
        "weather": info_list["weather"][0],
    }

    return weather_dict
