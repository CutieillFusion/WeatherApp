import pygame
import requests
from io import BytesIO
from PIL import Image
import datetime
from settings import *
import json

# requests weather data by calling with the city name
# returns a json style dictionary from the API
def request_current_weather_from_name_redundant(city_name:str) -> dict:
    # removes spaces just in case
    api_url = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name.replace(' ', '') + '&appid=' + OPEN_WEATHER_API_KEY

    # make a GET request
    response = requests.get(api_url)

    # check if the request was successful (status code 200)
    if response.status_code == 200:
        # parse and use the response data
        data = response.json()  # assumes the response is in JSON format
        return data
    else:
        # print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return None

# finds the city id from the city name
def find_city_id_from_name(name:str) -> int:
    # opens json file from path
    with open(PARSED_CITIES_PATH, 'r', encoding='utf-8', errors='ignore') as json_file:
        data = json.load(json_file)
    
    # loops through each entry till it finds a matching name
    for entry in data:
        if entry['name'] == name:
            return entry['id']
    return None

# requests current weather data using city name or city id
# returns a json style dictionary from API
def request_current_weather_from_name(name:str) -> dict:
    city_id = find_city_id_from_name(name)
    if city_id != None:
        api_url = 'https://api.openweathermap.org/data/2.5/weather?id=' + str(city_id) + '&appid=' + OPEN_WEATHER_API_KEY

        # make a GET request
        response = requests.get(api_url)

        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # parse and use the response data
            data = response.json()  # assumes the response is in JSON format
            return data
        else:
            # print an error message if the request was not successful
            print(f"Error: {response.status_code} - {response.text}")
            return None
    else:
        # runs api call using name mainly a fail safe
        return request_current_weather_from_name_redundant(name)
        
# requests weather data using lat and lon
# returns a json style dictionary from the API
def get_current_weather_from_coords(position:tuple=DEFAULT_COORDS) -> dict:
    api_url = 'https://api.openweathermap.org/data/2.5/weather?lat=' + str(position[0]) + '&lon=' + str(position[1]) + '&appid=' + OPEN_WEATHER_API_KEY

    # make a GET request
    response = requests.get(api_url)

    # check if the request was successful (status code 200)
    if response.status_code == 200:
        # parse and use the response data
        data = response.json()  # assumes the response is in JSON format
        return data
    else:
        # print an error message if the request was not successful
        print(f"Error: {response.status_code} - {response.text}")
        return None

# downloads image from a url
# returns a pillow image
def download_image(url:str) -> Image:
    # makes a GET request
    response = requests.get(url)
    
    # check if the request was successful (status code 200)
    if response.status_code == 200:
        # opens image
        image = Image.open(BytesIO(response.content))
        return image
    else:
        # print an error message if the request was not successful
        print(f"Failed to download image. Status code: {response.status_code}")
        return None

# converts pillow image to pygame surface
def convert_pillow_to_pygame_surface(pillow_image:Image) -> pygame.image:
    # convert Pillow image to raw RGBA format
    image_data = pillow_image.convert("RGBA").tobytes()

    # create a Pygame surface from the raw image data
    pygame_surface = pygame.image.fromstring(image_data, pillow_image.size, "RGBA")

    return pygame_surface

# downloads weather icon from OpenWeatherMap based on current weather conditions
def get_weather_icon(data:dict) -> pygame.image:
    # image url plus indexing for weather condition image 
    image_url = 'https://openweathermap.org/img/wn/' + data['weather'][0]['icon'] + '@4x.png'
    # downloads image
    downloaded_image = download_image(image_url)

    if downloaded_image:
        # convert Pillow image to Pygame surface
        return convert_pillow_to_pygame_surface(downloaded_image)
    
# unix timestamp to utc plus an offset by timezone
def unix_to_utc(unix_timestamp:int, local_time:int=0) -> datetime.datetime:
    # converts from unix to local time
    return datetime.datetime.utcfromtimestamp(unix_timestamp + local_time)

# converts unix timestamp into local time then returns hours and minutes
def unix_to_hour_minute(unix_timestamp:int, local_time:int=0) -> str:
    # grabs hours and minutes
    return str(unix_to_utc(unix_timestamp, local_time))[11:-3]

# converts unix timestamp into local time then returns day of the week
def unix_to_day_of_week(unix_timestamp:int, local_time:int=0) -> str:
    # grabs day of week
    return str(unix_to_utc(unix_timestamp, local_time).strftime("%A"))