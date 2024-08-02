import requests
import schedule
import time
import os
from git import Repo
from datetime import datetime

def get_weather_category(api_key, city):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': city,
        'aqi': 'no'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_code = data['current']['condition']['code']
        weather_text = data['current']['condition']['text']
        temperature = data['current']['temp_c']
        
        rainy_conditions = [1063, 1069, 1072, 1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 
                            1192, 1195, 1198, 1201, 1240, 1243, 1246, 1273, 1276]
        sunny_conditions = [1000]
        
        if weather_code in rainy_conditions:
            category = "rainy"
        elif weather_code in sunny_conditions:
            category = "sunny"
        else:
            category = "neutral"
        
        return category, weather_text, temperature
    else:
        print("Failed to retrieve data:", response.status_code, response.text)
        return None, None, None

def update_html(category):
    html_file = 'index.html'  # Path to your HTML file
    with open(html_file, 'r') as file:
        content = file.read()
    
    if category == 'rainy':
        new_content = content.replace('sun-icon.png', 'umbrella-icon.png')
    elif category == 'sunny':
        new_content = content.replace('umbrella-icon.png', 'sun-icon.png')
    else:
        new_content = content.replace('sun-icon.png', 'neutral-icon.png').replace('umbrella-icon.png', 'neutral-icon.png')
    
    with open(html_file, 'w') as file:
        file.write(new_content)
    
    return "HTML file updated"

def git_push():
    try:
        repo = Repo('C:/my projects/umbrella')
        repo.git.add(update=True)
        repo.index.commit('Update weather icon')
        origin = repo.remote(name='origin')
        origin.push()
        return "Changes pushed to Git"
    except Exception as e:
        return f"Error occurred while pushing to Git: {str(e)}"

def update_weather():
    global last_update, current_category, current_weather, current_temp, html_status, git_status
    
    api_key = '6afc27086b8749619c5222220243007'
    city = 'Sindelfingen'
    
    category, weather_text, temperature = get_weather_category(api_key, city)
    if category:
        current_category = category
        current_weather = weather_text
        current_temp = temperature
        html_status = update_html(category)
        git_status = git_push()
        last_update = datetime.now()
        print(f"Updated weather to {category}")

def print_status():
    current_time = datetime.now()
    time_since_update = current_time - last_update if last_update else None
    
    print("\n--- Status Update ---")
    print(f"Current time: {current_time}")
    print(f"Last update: {last_update}")
    print(f"Time since last update: {time_since_update}")
    print(f"Current weather: {current_weather}")
    print(f"Current temperature: {current_temp}°C")
    print(f"Assigned category: {current_category}")
    print(f"HTML status: {html_status}")
    print(f"Git status: {git_status}")
    print("---------------------\n")

# Initialize global variables
last_update = None
current_category = None
current_weather = None
current_temp = None
html_status = "Not updated yet"
git_status = "No push attempted yet"

# Schedule the weather update to run every hour
schedule.every().minute.do(update_weather)

# Run the initial update
update_weather()

# Main loop
while True:
    schedule.run_pending()
    print_status()
    time.sleep(5)  # Wait for 5 seconds before next status update