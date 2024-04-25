import os
import logging
from netCDF4 import Dataset, num2date
import numpy as np
import pandas as pd
import cdsapi
import configparser
from datetime import datetime, timedelta
import time
import math
from math import pi, radians, cos
from confluent_kafka import Producer
import json
import pymongo
import metpy.calc as mpcalc
from metpy.units import units

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    filemode='w', format='%(name)s-%(levelname)s-%(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def init_WeatherData(collection):

  WeatherData = [
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99950.41054316147,
                "sea_temp": 281.2021484375,
                "temperature": 281.5177712119097,
                "time": "12/03/2024 03:00:00",
                "total_cloud_cover": 99.15631044097071,
                "total_rain_water": 0.0,
                "total_snow_water": 0.17701392405935334
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99935.4852917614,
                "sea_temp": 281.2021484375,
                "temperature": 281.31876428649036,
                "time": "12/03/2024 04:00:00",
                "total_cloud_cover": 99.75108381053175,
                "total_rain_water": 0.0007095979682254956,
                "total_snow_water": 0.3757753792188977
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99927.18011154686,
                "sea_temp": 281.2021484375,
                "temperature": 281.74651765295835,
                "time": "12/03/2024 05:00:00",
                "total_cloud_cover": 97.56940662048655,
                "total_rain_water": 0.01694375820115836,
                "total_snow_water": 0.3873937129974365
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99870.51832044544,
                "sea_temp": 281.2021484375,
                "temperature": 282.3270990858546,
                "time": "12/03/2024 06:00:00",
                "total_cloud_cover": 96.00269883971582,
                "total_rain_water": 0.038085244596004486,
                "total_snow_water": 0.21331543109448903
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99864.04870542322,
                "sea_temp": 281.2021484375,
                "temperature": 282.75790901365116,
                "time": "12/03/2024 07:00:00",
                "total_cloud_cover": 99.97576475234386,
                "total_rain_water": 0.011639498859639844,
                "total_snow_water": 0.05470897415359971
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99830.13588621381,
                "sea_temp": 281.2021484375,
                "temperature": 282.80326177498586,
                "time": "12/03/2024 08:00:00",
                "total_cloud_cover": 100.0,
                "total_rain_water": 0.009748399933672795,
                "total_snow_water": 0.07182402959031176
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99814.2477153686,
                "sea_temp": 281.2021484375,
                "temperature": 282.70470832458096,
                "time": "12/03/2024 09:00:00",
                "total_cloud_cover": 99.96415202950864,
                "total_rain_water": 0.017325581186518023,
                "total_snow_water": 0.12507858342381334
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99814.18753290328,
                "sea_temp": 281.2021484375,
                "temperature": 282.6417596831657,
                "time": "12/03/2024 10:00:00",
                "total_cloud_cover": 97.21042201458002,
                "total_rain_water": 0.016389330304608707,
                "total_snow_water": 0.21877165059307574
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99727.49469160577,
                "sea_temp": 281.2021484375,
                "temperature": 283.299002978573,
                "time": "12/03/2024 11:00:00",
                "total_cloud_cover": 98.79833563704985,
                "total_rain_water": 0.01130591226360263,
                "total_snow_water": 0.0784027375117254
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99666.6502191644,
                "sea_temp": 281.2021484375,
                "temperature": 283.5878893290053,
                "time": "12/03/2024 12:00:00",
                "total_cloud_cover": 91.92057431263517,
                "total_rain_water": 0.008643612269793459,
                "total_snow_water": 0.05719117793397477
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99644.77389301955,
                "sea_temp": 281.2021484375,
                "temperature": 283.90048468217543,
                "time": "12/03/2024 13:00:00",
                "total_cloud_cover": 95.47760180716618,
                "total_rain_water": 0.008104875728806533,
                "total_snow_water": 0.09092369084676423
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99551.31052437323,
                "sea_temp": 281.2021484375,
                "temperature": 284.05760845641686,
                "time": "12/03/2024 14:00:00",
                "total_cloud_cover": 93.51858595496174,
                "total_rain_water": 0.0051386283661341865,
                "total_snow_water": 0.06507752700775385
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99533.88770066226,
                "sea_temp": 281.2021484375,
                "temperature": 284.25578928417985,
                "time": "12/03/2024 15:00:00",
                "total_cloud_cover": 94.0371192746045,
                "total_rain_water": 0.0015005585208503133,
                "total_snow_water": 0.04808976407259949
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99524.7399659332,
                "sea_temp": 281.2021484375,
                "temperature": 283.9519505661672,
                "time": "12/03/2024 16:00:00",
                "total_cloud_cover": 87.53399448687428,
                "total_rain_water": 0.0010245874021142937,
                "total_snow_water": 0.029250473842060476
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99543.66735127722,
                "sea_temp": 281.2021484375,
                "temperature": 282.9353547902393,
                "time": "12/03/2024 17:00:00",
                "total_cloud_cover": 84.16882936962102,
                "total_rain_water": 0.00016679329801860474,
                "total_snow_water": 0.015005285713194677
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99542.43361073811,
                "sea_temp": 281.2021484375,
                "temperature": 282.68686461520343,
                "time": "12/03/2024 18:00:00",
                "total_cloud_cover": 72.84137559534092,
                "total_rain_water": 0.00016679329801860474,
                "total_snow_water": 0.008218280971050235
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99544.3895408611,
                "sea_temp": 281.2021484375,
                "temperature": 282.1433749670781,
                "time": "12/03/2024 19:00:00",
                "total_cloud_cover": 73.12664465629337,
                "total_rain_water": 0.0,
                "total_snow_water": 0.027919688598502745
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99559.01387993454,
                "sea_temp": 281.2021484375,
                "temperature": 281.8910021330573,
                "time": "12/03/2024 20:00:00",
                "total_cloud_cover": 78.41144334830986,
                "total_rain_water": 0.0,
                "total_snow_water": 0.036552434613233764
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99508.67124769201,
                "sea_temp": 281.2021484375,
                "temperature": 281.64631200724074,
                "time": "12/03/2024 21:00:00",
                "total_cloud_cover": 87.46482305085573,
                "total_rain_water": 0.0,
                "total_snow_water": 0.027653531549791194
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99459.53226475594,
                "sea_temp": 281.248046875,
                "temperature": 281.56824577871384,
                "time": "12/03/2024 22:00:00",
                "total_cloud_cover": 90.48362608702335,
                "total_rain_water": 0.0,
                "total_snow_water": 0.02499774708547381
            },
            {
                "humidity": 96.57926147146746,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "pressure": 99505.69221565854,
                "sea_temp": 281.248046875,
                "temperature": 280.9841947356608,
                "time": "12/03/2024 23:00:00",
                "total_cloud_cover": 90.56491514686998,
                "total_rain_water": 0.0,
                "total_snow_water": 0.029163683500089327
            }
        ]
  
  df = pd.DataFrame(WeatherData)
  df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
  df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
  df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
  data = df.to_dict('records')
  collection.insert_many(data)
  

def init_WindData(collection):

  WindData = [
            {
                "direction": 131.56924028342664,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.4688136116430126,
                "time": "12/03/2024 03:00:00",
                "u10": -2.595208225425166,
                "v10": 2.3016433561708474
            },
            {
                "direction": 135.72998165508946,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.4990158458371106,
                "time": "12/03/2024 04:00:00",
                "u10": -2.4424554113411605,
                "v10": 2.5054986435896294
            },
            {
                "direction": 137.50480325283522,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.086868571286054,
                "time": "12/03/2024 05:00:00",
                "u10": -2.7607957762749824,
                "v10": 3.01338703134329
            },
            {
                "direction": 132.8101900444412,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.987847811702837,
                "time": "12/03/2024 06:00:00",
                "u10": -3.6591301170274493,
                "v10": 3.3896006519015573
            },
            {
                "direction": 136.6916005331812,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.005373427494936,
                "time": "12/03/2024 07:00:00",
                "u10": -4.119235983510908,
                "v10": 4.36994335384467
            },
            {
                "direction": 140.88500443190614,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.567891610711149,
                "time": "12/03/2024 08:00:00",
                "u10": -4.1435441970825195,
                "v10": 5.095904404212629
            },
            {
                "direction": 146.82139535213233,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.7572793998190175,
                "time": "12/03/2024 09:00:00",
                "u10": -3.697926025887741,
                "v10": 5.655631529217631
            },
            {
                "direction": 150.51258850832522,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.164192048273712,
                "time": "12/03/2024 10:00:00",
                "u10": -3.034214562528466,
                "v10": 5.365706439653688
            },
            {
                "direction": 155.17133068390297,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.089444165664456,
                "time": "12/03/2024 11:00:00",
                "u10": -2.556995713690593,
                "v10": 5.52658150821218
            },
            {
                "direction": 163.74414919744214,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 6.122976948356248,
                "time": "12/03/2024 12:00:00",
                "u10": -1.7139868670271134,
                "v10": 5.878188133239746
            },
            {
                "direction": 166.91125822854514,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 5.729231466181619,
                "time": "12/03/2024 13:00:00",
                "u10": -1.297441319263982,
                "v10": 5.580388805105978
            },
            {
                "direction": 162.77590219369836,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.843963877539972,
                "time": "12/03/2024 14:00:00",
                "u10": -1.434345178099297,
                "v10": 4.6267310227606036
            },
            {
                "direction": 167.60994338716006,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 4.090979120068913,
                "time": "12/03/2024 15:00:00",
                "u10": -0.8777843201636847,
                "v10": 3.9956982929288585
            },
            {
                "direction": 168.02186100041263,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.6401222410745815,
                "time": "12/03/2024 16:00:00",
                "u10": -0.7554653894713366,
                "v10": 3.5608653407952335
            },
            {
                "direction": 166.76931475702065,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.770198510562419,
                "time": "12/03/2024 17:00:00",
                "u10": -0.6340215544675665,
                "v10": 2.696667657757028
            },
            {
                "direction": 172.5546377476847,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.4564346322807227,
                "time": "12/03/2024 18:00:00",
                "u10": -0.31830647659947897,
                "v10": 2.4357241407070207
            },
            {
                "direction": 188.84602224762565,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.879656272951848,
                "time": "12/03/2024 19:00:00",
                "u10": 0.442832306754814,
                "v10": 2.8454032751870404
            },
            {
                "direction": 211.24631336524436,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 3.105333881060079,
                "time": "12/03/2024 20:00:00",
                "u10": 1.6107933524435936,
                "v10": 2.6548904475671273
            },
            {
                "direction": 237.71925301942457,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 2.635802543730374,
                "time": "12/03/2024 21:00:00",
                "u10": 2.2284164428710938,
                "v10": 1.4076985496466392
            },
            {
                "direction": 257.8136366662268,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 1.6348963362448974,
                "time": "12/03/2024 22:00:00",
                "u10": 1.5980558485320695,
                "v10": 0.3451138004186962
            },
            {
                "direction": 281.02979039349015,
                "latitude": 43.24399948120117,
                "longitude": 27.92099952697754,
                "speed": 1.3366883096066495,
                "time": "12/03/2024 23:00:00",
                "u10": 1.3119967912213477,
                "v10": -0.2557343482287222
            }
        ]
  
  df = pd.DataFrame(WindData)
  df['time'] = pd.to_datetime(df['time'], format='%d/%m/%Y %H:%M:%S')
  df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
  df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
  data = df.to_dict('records')
  collection.insert_many(data)
  
def delivery_report(err, msg):
    if err is not None:
        logging.error('Failed to deliver message: %s', err)
    else:
        logging.info('Message delivered to topic: %s', msg.topic())


def create_square(lat1, lon1, distance_km):
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    bearing_list_lat = [0, 180]
    bearing_list_lon = [90, 270]

    # Convert bearing from degrees to radians
    bearing_90 = math.radians(bearing_list_lon[0])
    bearing_270 = math.radians(bearing_list_lon[1])
    bearing_0 = math.radians(bearing_list_lat[0])
    bearing_180 = math.radians(bearing_list_lat[1])

    # Calculate new latitude
    lat2_0 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_0))
    
    # Calculate new latitude
    lat2_180 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_180))
    
     # Calculate new latitude
    lat2_90 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_90))
    
    # Calculate new latitude
    lat2_270 = math.asin(math.sin(lat1) * math.cos(distance_km / R) +
                     math.cos(lat1) * math.sin(distance_km / R) * math.cos(bearing_270))

    # Calculate new longitude
    lon2_90 = lon1 + math.atan2(math.sin(bearing_90) * math.sin(distance_km / R) * math.cos(lat1),
                             math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2_90))
    
    # Calculate new longitude
    lon2_270 = lon1 + math.atan2(math.sin(bearing_270) * math.sin(distance_km / R) * math.cos(lat1),
                             math.cos(distance_km / R) - math.sin(lat1) * math.sin(lat2_270))

    # Convert latitude and longitude back to degrees
    lat2_0 = math.degrees(lat2_0)
    lat2_180 = math.degrees(lat2_180)
    lon2_90 = math.degrees(lon2_90)
    lon2_270 = math.degrees(lon2_270)

    return lat2_180, lon2_270, lat2_0, lon2_90


producer = Producer({'bootstrap.servers': 'kafka1:29092'})
topic_metadata = producer.list_topics()
topic_list = topic_metadata.topics
for topic in topic_list:
    logging.info("----------------------------------------------- %s", topic)
topic = 'wind_topic'
topic_weather = 'weather_topic'
myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol = db["windData"]

mycolweather = db["weatherData"]
mycolweather.drop()

while True:
    try:
        logging.info('emptyBefore')
        init_WeatherData(mycolweather)

        if mycol.count_documents({}) == 0:
          init_WindData(mycol)
          init_WeatherData(mycolweather)
          logging.info('empty')
          
        config = configparser.ConfigParser()
        config.read('config.conf')
        lon, lat, rad = map(float,
                            [config.get('Default', 'longitude'),
                             config.get('Default', 'latitude'),
                             config.get('Default', 'radius')]
                            )
        lat_min, lon_min, lat_max, lon_max = create_square(lat, lon, rad)
        curr_time = datetime.now() - timedelta(days=6)
        mon_curr, day_curr = curr_time.strftime("%m"), curr_time.strftime("%d")
        c = cdsapi.Client()
        windData = 'data/ERA5_Weather3H.nc'
        dataList = [{'fileLocation': windData,
                     'month': mon_curr,
                     'day': day_curr}]
        logging.info("month %s", dataList[0]["month"])
        logging.info("day %s", dataList[0]["day"])

        for item in dataList:
            c.retrieve('reanalysis-era5-single-levels',
                       {'product_type': 'reanalysis',
                        'variable': ['10m_u_component_of_wind',
                                     '10m_v_component_of_wind', 
                                     '2m_temperature', 
                                     '2m_dewpoint_temperature',
                                     'sea_surface_temperature',
                                     'total_cloud_cover', 
                                     'total_column_rain_water',
                                     'total_column_snow_water',
                                     'surface_pressure'
                                    ],
                        'year': '2024',
                        'month': item['month'],
                        'day': item['day'],
                        'time': [f'{i:02d}:00' for i in range(24)],
                        'area': [lat_max,
                                 lon_min,
                                 lat_min,
                                 lon_max],
                        'format': 'netcdf'},
                       item['fileLocation'])

        with Dataset('data/ERA5_Weather3H.nc', 'r+') as windData_BL:
            for var_name in windData_BL.variables.keys():
                variable = windData_BL.variables[var_name]
                logging.info(f'Variable Name: {var_name}')
                logging.info(f'Dimensions: {variable.dimensions}')
                logging.info(f'Shape: {variable.shape}')
                logging.info(f'Units: {variable.units if "units" in variable.ncattrs() else "N/A"}')
                logging.info(f'Description: {variable.long_name if "long_name" in variable.ncattrs() else "N/A"}')
                logging.info('\n')
            u10, v10, tem, dewpoint_temp, sea_temp, total_cloud_cover, total_rain_water, total_snow_water, pressure, = map(windData_BL.variables.get, ['u10', 'v10', 't2m', 'd2m', 'sst', 'tcc', 'tcrw', 'tcsw', 'sp'])
          
            logging.info(f'u10: {u10}')
            logging.info(f'v10: {v10}')
            logging.info(f'tem: {tem}')
            logging.info(f'dewpoint_temp: {dewpoint_temp}')
            logging.info(f'sea_temp: {sea_temp}')
            logging.info(f'total_cloud_cover: {total_cloud_cover}')
            logging.info(f'pressure: {pressure}')
            logging.info(f'total_rain_water: {total_rain_water}')
            logging.info(f'total_snow_water: {total_snow_water}')
          
            wind_speed = np.sqrt(u10[:]**2 + v10[:]**2)
            wind_dir = (270 - np.arctan2(v10[:], u10[:]) * 180 / pi) % 360
            time_dim, lat_dim, lon_dim = u10.get_dims()
            time_var = windData_BL.variables[time_dim.name]
            times = num2date(time_var[:], time_var.units)
            latitudes = windData_BL.variables[lat_dim.name][:]
            longitudes = windData_BL.variables[lon_dim.name][:]
            times_grid, latitudes_grid, longitudes_grid = [x.flatten()
                                                           for x
                                                           in np.meshgrid(
                                                               times,
                                                               latitudes,
                                                               longitudes,
                                                               indexing='ij')]

            if tem[:].flatten() is not None and dewpoint_temp[:].flatten() is not None:
              temp = tem[:].flatten()[0]
              dew = dewpoint_temp[:].flatten()[0]
              logging.info(f'tem: {temp}')
              logging.info(f'dew: {dew}')
              relative_humidity = mpcalc.relative_humidity_from_dewpoint(tem[:].flatten()[0] * units.degC, dewpoint_temp[:].flatten()[0] * units.degC)
            else:
              relative_humidity = 0

            df = pd.DataFrame({'time': [t.isoformat(sep=" ")
                                        for t in times_grid],
                               'latitude': latitudes_grid,
                               'longitude': longitudes_grid,
                               'u10': u10[:].flatten(),
                               'v10': v10[:].flatten(),
                               'speed': wind_speed.flatten(),
                               'direction': wind_dir.flatten()})

            df_weather = pd.DataFrame({'time': [t.isoformat(sep=" ") for t in times_grid],
                                     'latitude': latitudes_grid,
                                     'longitude': longitudes_grid,
                                     'temperature': tem[:].flatten(),
                                     'humidity': relative_humidity.magnitude * 100,
                                     'sea_temp': sea_temp[:].flatten(),
                                     'total_cloud_cover': total_cloud_cover[:].flatten() * 100,
                                     'pressure': pressure[:].flatten(),
                                     'total_rain_water': total_rain_water[:].flatten(),
                                     'total_snow_water': total_snow_water[:].flatten()})

          

            df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
            df_weather['time'] = pd.to_datetime(df_weather['time'], format='%Y-%m-%d %H:%M:%S')

            logging.info(df)
            logging.info(df_weather)
            df.dropna(subset=['u10'], inplace=True)
            df_weather.dropna(subset=['sea_temp'], inplace=True)
            logging.info(df)
            logging.info(df_weather)
            data = df.to_dict(orient='records')
            mycol.insert_many(data)
            data_weather = df_weather.to_dict(orient='records')
            mycolweather.insert_many(data_weather)

        # Convert it back to string format
        df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        for index, row in df.iterrows():
            value = json.dumps(row.to_dict()).encode('utf-8')
            producer.produce(topic=topic,
                             value=value,
                             callback=delivery_report)
            producer.flush()

        df_weather['time'] = df_weather['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        for index, row in df_weather.iterrows():
            value = json.dumps(row.to_dict()).encode('utf-8')
            producer.produce(topic=topic_weather,
                             value=value,
                             callback=delivery_report)
            producer.flush()

        os.remove(windData)
        logging.info("File deleted successfully.")
    except FileNotFoundError:
        logging.error("File not found.")
    except Exception as e:
        logging.error("Error: %s", e)
    time.sleep(24 * 60 * 60)
