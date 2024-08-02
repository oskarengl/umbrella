import requests

def get_weather_category(weather_code):
    rainy_conditions = [
        1063, 1069, 1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 
        1192, 1195, 1198, 1201, 1240, 1243, 1246, 1273, 1276
    ]
    sunny_conditions = [1000]
    neutral_conditions = [
        1003, 1006, 1009, 1030, 1066, 1087, 1114, 1117, 1135, 1147, 
        1204, 1207, 1210, 1213, 1216, 1219, 1222, 1225, 1237, 1249, 
        1252, 1255, 1258, 1261, 1264, 1279, 1282
    ]
    
    if weather_code in rainy_conditions:
        return "rainy"
    elif weather_code in sunny_conditions:
        return "sunny"
    else:
        return "neutral"

def get_weather(api_key, city):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'no'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_text = data['current']['condition']['text']
        weather_code = data['current']['condition']['code']
        category = get_weather_category(weather_code)
        print(f"Current weather in {city}:")
        print(f"Weather: {weather_text}")
        print(f"Category: {category}")
    else:
        print("Failed to retrieve data:", response.status_code, response.text)

# Replace with your API key and desired city
api_key = '6afc27086b8749619c5222220243007'
city = 'Singapore'

get_weather(api_key, city)