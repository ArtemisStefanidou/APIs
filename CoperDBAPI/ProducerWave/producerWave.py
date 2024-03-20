import configparser
import json
import os
import time
from datetime import datetime, timedelta
from math import cos, radians
import logging
import motuclient
import numpy as np
import pandas as pd
import pymongo
from confluent_kafka import Producer
from netCDF4 import Dataset, num2date
import math

# Configure logging
logging.basicConfig(level=logging.INFO, filename='app.log',
                    filemode='w', format='%(name)s-%(levelname)s-%(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


# def create_square(latitude, longitude, radius):
  
#     radius_in_degrees = radius / 111.00
#     min_latitude = latitude - radius_in_degrees
#     max_latitude = latitude + radius_in_degrees
#     min_longitude = longitude - radius_in_degrees
#     max_longitude = longitude + radius_in_degrees

#     return min_latitude, min_longitude, max_latitude, max_longitude
def init_WaveData(collection):

  WaveData = [
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "13/03/2024 12:00:00",
                "vhm0": 0.6299999952316284,
                "vmdr": 86.0999984741211,
                "vtm10": 6.37999963760376
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "13/03/2024 15:00:00",
                "vhm0": 0.5999999642372131,
                "vmdr": 85.3499984741211,
                "vtm10": 6.019999980926514
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "13/03/2024 18:00:00",
                "vhm0": 0.550000011920929,
                "vmdr": 85.74000549316406,
                "vtm10": 6.159999847412109
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "13/03/2024 21:00:00",
                "vhm0": 0.5199999809265137,
                "vmdr": 87.05000305175781,
                "vtm10": 6.099999904632568
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 00:00:00",
                "vhm0": 0.4699999988079071,
                "vmdr": 86.70999908447266,
                "vtm10": 6.029999732971191
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 03:00:00",
                "vhm0": 0.41999998688697815,
                "vmdr": 86.24000549316406,
                "vtm10": 5.909999847412109
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 06:00:00",
                "vhm0": 0.3700000047683716,
                "vmdr": 85.69000244140625,
                "vtm10": 5.799999713897705
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 09:00:00",
                "vhm0": 0.3499999940395355,
                "vmdr": 84.06000518798828,
                "vtm10": 5.799999713897705
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 12:00:00",
                "vhm0": 0.3199999928474426,
                "vmdr": 83.95000457763672,
                "vtm10": 5.690000057220459
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 15:00:00",
                "vhm0": 0.28999999165534973,
                "vmdr": 83.75,
                "vtm10": 5.579999923706055
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 18:00:00",
                "vhm0": 0.26999998092651367,
                "vmdr": 82.26000213623047,
                "vtm10": 5.329999923706055
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "14/03/2024 21:00:00",
                "vhm0": 0.29999998211860657,
                "vmdr": 74.19000244140625,
                "vtm10": 4.929999828338623
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "15/03/2024 00:00:00",
                "vhm0": 0.3199999928474426,
                "vmdr": 72.56000518798828,
                "vtm10": 5.029999732971191
            },
            {
                "latitude": 43.0,
                "longitude": 27.916666666666657,
                "time": "15/03/2024 03:00:00",
                "vhm0": 0.3199999928474426,
                "vmdr": 69.61000061035156,
                "vtm10": 5.029999732971191
            }
        ]
  collection.insert_many(WaveData)

def create_square(lat1, lon1, distance_km):
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    bearing_list_lat = [0, 180]
    bearing_list_lon = [90, 270] #τα διαφορετικα

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

class MotuOptions:
    def __init__(self, attrs: dict):
        super(MotuOptions, self).__setattr__("attrs", attrs)

    def __setattr__(self, k, v):
        self.attrs[k] = v

    def __getattr__(self, k):
        try:
            return self.attrs[k]
        except KeyError:
            return None


def motu_option_parser(script_template, usr, pwd, output_filename):
    dictionary = dict(
        [e.strip().partition(" ")[::2] for e in script_template.split('--')])
    dictionary['variable'] = [value for (var, value) in
                              [e.strip().partition(" ")[::2]
                               for e in script_template.split('--')]
                              if var == 'variable']
    for k, v in list(dictionary.items()):
        if v == '<OUTPUT_DIRECTORY>':
            dictionary[k] = '.'
        if v == '<OUTPUT_FILENAME>':
            dictionary[k] = output_filename
        if v == '<USERNAME>':
            dictionary[k] = usr
        if v == '<PASSWORD>':
            dictionary[k] = pwd
        if k in ['longitude-min', 'longitude-max', 'latitude-min',
                 'latitude-max', 'depth-min', 'depth-max']:
            dictionary[k] = float(v)
        if k in ['date-min', 'date-max']:
            dictionary[k] = v[1:-1]
        dictionary[k.replace('-', '_')] = dictionary.pop(k)
    dictionary.pop('python')
    dictionary['auth_mode'] = 'cas'
    return dictionary


# Create the Kafka producer
producer = Producer({
    'bootstrap.servers': 'kafka1:29092'
})
topic_metadata = producer.list_topics()
topic_list = topic_metadata.topics
for topic in topic_list:
    logging.info("------------------------------------------", topic)
topic = 'wave_topic'


def delivery_report(err, msg):
    if err is not None:
        logging.info(f'Failed to deliver message: {err}')
    else:
        logging.info(f'Message delivered to topic: {msg.topic()}')


myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol = db["waveData"]
logging.info('waveData')

if mycol.count_documents({}) == 0:
    init_WaveData(mycol)
    logging.info('empty')


while True:

    myclient = pymongo.MongoClient("mongodb://mongodb:27017")
    db = myclient["kafka_db"]
    mycol = db["waveData"]

    config = configparser.ConfigParser()
    config.read('config.conf')

    lon = float(config.get('Default', 'longitude'))
    lat = float(config.get('Default', 'latitude'))
    rad = float(config.get('Default', 'radius'))

    lat_min, lon_min, lat_max, lon_max = create_square(lat, lon, rad)

    # Get the current time
    curr_time = datetime.now()
    curr_time = datetime.now()
    delta_3h = curr_time - timedelta(hours=3)
    delta_3h = delta_3h + timedelta(seconds=1)

    USERNAME = 'capi'
    PASSWORD = 'copernicusPass!1'
    OUTPUT_FILENAME = 'data/CMEMS_Wave3H.nc'

    # Change the variables according to the desired dataset
    script_template = f'python -m motuclient \
        --motu https://nrt.cmems-du.eu/motu-web/Motu \
        --service-id GLOBAL_ANALYSISFORECAST_WAV_001_027-TDS \
        --product-id cmems_mod_glo_wav_anfc_0.083deg_PT3H-i \
        --longitude-min {lon_min} --longitude-max {lon_max} \
        --latitude-min {lat_min} --latitude-max {lat_max} \
        --date-min "' + str(delta_3h) + '" --date-max "' + str(curr_time) + '" \
        --variable VHM0 --variable VMDR --variable VTM10 \
        --out-dir <OUTPUT_DIRECTORY> --out-name <OUTPUT_FILENAME> \
        --user <USERNAME> --pwd <PASSWORD>'

    logging.info(script_template)

    data_request_options_dict_automated = motu_option_parser(script_template, USERNAME, PASSWORD, OUTPUT_FILENAME)

    # Motu API executes the downloads
    motuclient.motu_api.execute_request(MotuOptions(data_request_options_dict_automated))

    waveData = Dataset('data/CMEMS_Wave3H.nc', 'r+')

    waveData.set_auto_mask(True)

    # Extract variables for wave dataset
    vhm0 = waveData.variables['VHM0']
    vmdr = waveData.variables['VMDR']
    vtm10 = waveData.variables['VTM10']

    # Get dimensions assuming 3D: time, latitude, longitude
    time_dim, lat_dim, lon_dim = vhm0.get_dims()
    time_var = waveData.variables[time_dim.name]
    times = num2date(time_var[:], time_var.units)
    latitudes = waveData.variables[lat_dim.name][:]
    longitudes = waveData.variables[lon_dim.name][:]

    times_grid, latitudes_grid, longitudes_grid = [x.flatten() for x in
                                                   np.meshgrid(times, latitudes, longitudes, indexing='ij')]

    df = pd.DataFrame({
        'time': [t.isoformat(sep=" ") for t in times_grid],
        'latitude': latitudes_grid,
        'longitude': longitudes_grid,
        'vhm0': vhm0[:].flatten(),
        'vmdr': vmdr[:].flatten(),
        'vtm10': vtm10[:].flatten(),
    })

    df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S')
  
    logging.info(df)

    # Find null values in 'Feature1'
    null_values = df['vhm0'].isnull()

    # Filter the DataFrame to show only rows with null values in 'Feature1'
    rows_with_null = df[null_values]

    # logging.info the rows with null values
    logging.info(rows_with_null)

    # Drop rows with null values in 'vhm0'
    df = df.dropna(subset=['vhm0'])

    logging.info(df)

    # Convert DataFrame to a list of dictionaries (JSON-like documents)
    data = df.to_dict(orient='records')

    mycol.insert_many(data)
    myclient.close()

    # Convert it back to string format
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    for index, row in df.iterrows():
        data_topic = row.to_dict()
        value = json.dumps(data_topic).encode('utf-8')
        producer.produce(topic=topic, value=value, callback=delivery_report)
        producer.flush()
    file_path = 'data/CMEMS_Wave3H.nc'
    try:
        os.remove(file_path)
        logging.info("File deleted successfully.")
    except FileNotFoundError:
        logging.info("File not found.")
    except Exception as e:
        logging.info(f"Error: {e}")
    time.sleep(3 * 3600)
