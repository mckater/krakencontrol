import requests
from config import *


def weather_by_city(city_name=DEFAULT_CITY):
    weather_url = WEATHER_URL
    params = {
        'key': WEATHER_API_KEY,
        'q': city_name,
        'format': 'json',
        'num_of_days': 1,
        'lang': 'en'
    }
    try:
        result = requests.get(weather_url, params=params)
        weather = result.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]["temp_C"], \
                           weather['data']['current_condition'][0]["weatherDesc"][0]['value'], \
                           weather['data']['current_condition'][0]["FeelsLikeC"]
                except(IndexError, TypeError):
                    return False
        return False
    except(requests.RequestException, ValueError):
        print('Internet request failed')
        return False


# if __name__ == '__main__':
#     print('В Городе {}, {}. Ощущается как {}'.format(*weather_by_city()))  # 'Moscow,Russia'
