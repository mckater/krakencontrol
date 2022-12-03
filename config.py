import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'yandexlyceum_secret_key'
DEFAULT_CITY = 'Moscow,Russia'
WEATHER_API_KEY = '5d20b324861d406ab66183759221911'
WEATHER_URL = 'ht_tp://api.worldweatheronline.com/premium/v1/weather.ashx'
# для удобства из любого расположения в разных ОС
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, ' .. ')
