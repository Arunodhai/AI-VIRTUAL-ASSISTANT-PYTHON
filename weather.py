import requests

#Use open weather API

def setCity(city_name):
    global api_address
    api_address = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=Your APP ID"
    global json_data
    json_data = requests.get(api_address).json()

def temp():
    temperature = round(json_data['main']['temp']-273,1)
    return temperature

def des():
    description = json_data['weather'][0]['description']
    return description

