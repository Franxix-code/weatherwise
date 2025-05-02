from django.shortcuts import render
import requests
from datetime import datetime

API_KEY = '80cd0bbffdbc236adbbb1c4b71e30557'

def get_weather_by_coords(lat, lon):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

def get_weather(city):
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json() if response.status_code == 200 else None

def get_forecast(city=None, lat=None, lon=None):
    base_url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'appid': API_KEY,
        'units': 'metric'
    }

    if city:
        params['q'] = city
    elif lat and lon:
        params['lat'] = lat
        params['lon'] = lon
    else:
        return {}

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        return {}

    forecast_raw = response.json()
    daily_forecast = {}

    for entry in forecast_raw['list']:
        day = datetime.fromtimestamp(entry['dt']).strftime('%A')

        if day not in daily_forecast:
            daily_forecast[day] = {
                'temp': round(entry['main']['temp']),
                'icon': entry['weather'][0]['icon'],
                'desc': entry['weather'][0]['description']
            }

        if len(daily_forecast) >= 5:
            break

    return daily_forecast

def home(request):
    city = request.GET.get('city')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')

    context = {
        'icon_url': 'https://openweathermap.org/img/wn/10d@2x.png',
        'weather': None,
        'weather_description': None,
        'city': None,
        'country': None,
        'wind_speed': None,
        'pressure': None,
        'humidity': None,
        'temperature': None,
        'forecast': {}  # New field for 5-day forecast
    }

    weather_data = None
    if lat and lon:
        weather_data = get_weather_by_coords(lat, lon)
        context['forecast'] = get_forecast(lat=lat, lon=lon)
    elif city:
        weather_data = get_weather(city)
        context['forecast'] = get_forecast(city=city)

    if weather_data:
        icon_id = weather_data['weather'][0]['icon']
        context.update({
            'icon_url': f'https://openweathermap.org/img/wn/{icon_id}@2x.png',
            'weather': weather_data['weather'][0]['main'],
            'weather_description': weather_data['weather'][0]['description'],
            'city': weather_data['name'],
            'country': weather_data['sys']['country'],
            'wind_speed': weather_data['wind']['speed'],
            'pressure': weather_data['main']['pressure'],
            'humidity': weather_data['main']['humidity'],
            'temperature': round(weather_data['main']['temp']),
        })

    return render(request, 'index.html', context)


    # return render(request, 'index.html', {
    #     'icon_url': icon_url,
    #     'weather': weather,
    #     'weather_description': weather_description,
    #     'city': city,
    #     'country': country,
    #     'wind_speed': wind_speed,
    #     'pressure': pressure,
    #     'humidity': humidity,
    #     'temperature': temperature,
    # })


    # return render(request, 'index.html')