import logging
from datetime import datetime, timedelta
from math import cos, radians
import math
import pymongo
from flask import Flask, jsonify, request, current_app
from pymongo import DESCENDING
import json
from bson import json_util
import re
from confluent_kafka import Producer
# from flask_cors import CORS
# import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="w",
    format="%(name)s-%(levelname)s-%(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(name)s-%(levelname)s-%(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)

app = Flask(__name__)
# CORS(app)

myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol_wave = db["waveData"]
mycol_wind = db["windData"]
mycol_living = db['living_lab']
mycol_dynamic = db["ais_cyprus_dynamic"]
mycol_static = db["ais_cyprus_static"]
mycol_weather = db["weatherData"]
collection = db['bulgaria']

def delivery_report(err, msg):
    if err is not None:
        logging.error('Failed to deliver message: %s', err)
    else:
        logging.info('Message delivered to topic: %s', msg.topic())

@app.route('/lab', methods=['POST'])
def add_data():
    try:
        producer = Producer({'bootstrap.servers': 'kafka1:29092'})
        topic_metadata = producer.list_topics()
        topic_list = topic_metadata.topics
        for topic in topic_list:
            logging.info("----------------------------------------------- %s", topic)
        topic = 'living_lab'
        
        json_data = request.data
        data_str = json_data.decode('utf-8')

        pattern = r'"id":(\w+)'
        data_with_quotes = re.sub(pattern, lambda x: f'"id":"{x.group(1)}"', data_str)

        data_list = json.loads(data_with_quotes)
        logging.info(f'data_list: {data_list}')

        for data_item in data_list:
            message_str = json.dumps(data_item)
            producer.produce(topic, value=message_str.encode('utf-8'), callback=delivery_report)
            producer.flush()
            mycol_living.insert_one(data_item)
        
        return jsonify({'message': 'Data added successfully'})
    except Exception as e:
        logging.info(f'error: {str(e)}')
        return jsonify({'error': str(e)})
            

@app.route('/living_lab', methods=['GET'])
def get_living_lab_data():
    try:
        date_min = datetime.strptime(request.args.get("dateMin"), "%Y-%m-%dT%H:%M:%S")
        date_max = datetime.strptime(request.args.get("dateMax"), "%Y-%m-%dT%H:%M:%S")

        results = mycol_living.find({
            'time': {
                '$gte': date_min.strftime("%d/%m/%Y %H:%M:%S"),
                '$lte': date_max.strftime("%d/%m/%Y %H:%M:%S")
            }
        }).sort('time', DESCENDING)

        data_list = list(results)
        logging.info(f'data_list: {data_list}')
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})

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
        
def search_data(
    start_date,
    end_date,
    min_longitude,
    max_longitude,
    min_latitude,
    max_latitude,
    database,
):
    query = {}
            
    query = {
            "time": {"$gte": start_date, "$lte": end_date},
            "longitude": {"$gte": min_longitude, "$lte": max_longitude},
            "latitude": {"$gte": min_latitude, "$lte": max_latitude},
    }

    last_data = database.find(query)

    if not last_data:
            return {database.name: []}
    else:
            data_list = []
            for document in last_data:
                data_list.append(document)
            for data in data_list:
                data.pop("_id", None)
                data['time'] = data['time'].strftime("%d/%m/%Y %H:%M:%S")
            if database == mycol_weather:
                logging.info(f'times: 1 ---------------------------------------------- : {data_list}')
            return {database.name: data_list}


@app.route("/data", methods=["GET"])
def get_data():
    latitude, longitude, radius = map(
        float,
        [
            request.args.get("latitude"),
            request.args.get("longitude"),
            request.args.get("radius"),
        ],
    )
    lat_min, lon_min, lat_max, lon_max = create_square(latitude,
                                                       longitude,
                                                       radius)

    date_format = "%Y-%m-%d %H:%M:%S"
    date_min = datetime.strptime(
        request.args.get("dateMin").replace("T", " "), date_format
    )
    date_max = datetime.strptime(
        request.args.get("dateMax").replace("T", " "), date_format
    )
    info_return = [
        search_data(date_min, date_max, lon_min,
                    lon_max, lat_min, lat_max, mycol_wave),
        search_data(date_min, date_max, lon_min,
                    lon_max, lat_min, lat_max, mycol_wind),
        search_data(date_min, date_max, lon_min,
                    lon_max, lat_min, lat_max, mycol_weather)
    ]
    return jsonify(info_return)

        
@app.route("/ais_cyprus_dynamic", methods=["GET"])
def get_ais_cyprus_dynamic():
    try:
        date_min = datetime.strptime(request.args.get("dateMin"), "%Y-%m-%dT%H:%M:%S")
        date_max = datetime.strptime(request.args.get("dateMax"), "%Y-%m-%dT%H:%M:%S")
        
        if date_max - date_min > timedelta(hours=2):
            date_min = date_max - timedelta(hours=2)

        results = mycol_dynamic.find({
                    'timestamp': {
                        '$gte': date_min.strftime("%d/%m/%Y %H:%M:%S"),
                        '$lte': date_max.strftime("%d/%m/%Y %H:%M:%S")
                    }
                })

        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route("/ais_static", methods=["GET"])
def get_ais_static():
    try:
        date_min = datetime.strptime(request.args.get("dateMin"), "%Y-%m-%dT%H:%M:%S")
        date_max = datetime.strptime(request.args.get("dateMax"), "%Y-%m-%dT%H:%M:%S")
        
        if date_max - date_min > timedelta(hours=2):
            date_min = date_max - timedelta(hours=2)

        results = mycol_static.find({
                    'timestamp': {
                        '$gte': date_min.strftime("%d/%m/%Y %H:%M:%S"),
                        '$lte': date_max.strftime("%d/%m/%Y %H:%M:%S")
                    }
                })

        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/weather", methods=["GET"])
def get_weather_data():
    try:
        results = mycol_weather.find()
        data_list = list(results)
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/data_info", methods=["GET"])
def data_info():
    try:
        result_dynamic = mycol_dynamic.delete_many({"shipId": {"$exists": True}})
        result_d = result_dynamic.deleted_count
        logging.info(f'dynamic: {result_d}')

        unique_mmsi_dynamic = mycol_dynamic.distinct("mmsi")
        logging.info(f'unique_mmsi: {unique_mmsi_dynamic}')

        result_static = mycol_static.delete_many({"shipId": {"$exists": True}})
        result_s = result_static.deleted_count
        logging.info(f'dynamic: {result_s}')

        unique_mmsi_static = mycol_static.distinct("mmsi")
        logging.info(f'unique_mmsi: {unique_mmsi_static}')

        unique_mmsi_ship_types = {}
        for mmsi in unique_mmsi_static:
            ship_type = mycol_static.find_one({"mmsi": mmsi}, {"ship_type": 1})
            unique_mmsi_ship_types[mmsi] = ship_type["ship_type"] if ship_type else None

        logging.info(f'Unique MMSI values with ship types:: {unique_mmsi_ship_types}')
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route("/bulgaria", methods=["GET"])
def get_athens_data():
    try:

        last_10_documents = collection.find()

        data_list = list(last_10_documents)
        logging.info(f'data_list: {data_list}')
        json_data = json.loads(json_util.dumps(data_list))
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'error': str(e)})
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
