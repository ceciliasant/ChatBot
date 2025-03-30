import requests

WTTR_URL = "https://wttr.in/{city}?format=j1"

def get_weather(city="Aveiro"):
    response = requests.get(WTTR_URL.format(city=city))
    
    if response.status_code == 200:
        data = response.json()
        current_condition = data["current_condition"][0]
        temp = current_condition["temp_C"]
        weather_desc = current_condition["weatherDesc"][0]["value"]
        return f"Currently, it's {weather_desc.lower()} with {temp}°C in {city}."

    else:
        return "Sorry, I couldn't fetch the weather right now."