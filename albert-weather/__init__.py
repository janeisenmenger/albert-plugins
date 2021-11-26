# -*- coding: utf-8 -*-


"""An Albert extension that allows you to talk to jira."""

from typing import ItemsView
from albert import *
import geocoder
import json
import requests


__title__ = "Weather"
__version__ = "0.0.1"
__triggers__ = "weather"
__authors__ = "Jan Eisenmenger"

def get_config_path(): 
    return configLocation() + '/weather.json'

def get_config():
    try:
        with open(get_config_path(), 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        info(str(e))
        return {}

def write_config(config):
    with open(get_config_path(), 'w+') as config_file:
            json.dump(config, config_file)

def write_icon(id):
    id = id.replace('n', 'd')
    
    icon_response = requests.get('http://openweathermap.org/img/wn/{}@2x.png'.format(id))
    info(icon_response.content)
    with open(dataLocation() + '/{}.png'.format(id), 'wb') as icon:
        icon.write(icon_response.content)
        
    return dataLocation() + '/{}.png'.format(id)

def change_weather_api_key(api_key, config):   
    def handle_enter_api_key(): 
        config['api_key'] = api_key
        write_config(config)
    
    return [Item(id = 'weather_openweathermap-api-key',
                text = 'Enter your openweathermap api key', 
                subtext = '', 
                actions = [
                    FuncAction(text= 'enter new openweathermap api key', callable=handle_enter_api_key)
                ]
        )] 

def check_valid_config(config, query):
    if config.get('api_key') == None:
        return change_weather_api_key(query.string, config)
        
    return

def get_current_weather(config, lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units=metric'.format(lat, lon, config['api_key'])
    weather_data = requests.get(url).json()
    
    temperature = int(round(float(weather_data['current']['temp']), 0))  
    
    weather_description = "{}°C | {}".format(temperature, weather_data['current']['weather'][0]['description'])
    weather_icon_location = write_icon(weather_data['current']['weather'][0]['icon'])
    
    return weather_description, weather_icon_location

def handleQuery(query):
    if not query.isTriggered:
        return
    
    config = get_config()
    valid_config_result = check_valid_config(config, query)
    
    if (valid_config_result != None):
        return valid_config_result
    
    query_tokens = query.string.split(' ')
    
    if (query_tokens[0] == 'change-api-key'):
        change_weather_api_key(query_tokens[0], config)
    
    location = geocoder.ip('me')
    
    weather_description, weather_icon_location = get_current_weather(config, location.latlng[0], location.latlng[1])
    info(weather_icon_location)
    return [Item(
                id = 'current-weather',
                icon = weather_icon_location,
                text = weather_description, 
                subtext = location.city, 
                actions = [
                ]
    )]
    
    
    
    
   
    