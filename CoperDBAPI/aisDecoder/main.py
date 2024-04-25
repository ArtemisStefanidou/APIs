import logging
import json
import pymongo
from datetime import datetime
from pyais import decode
from pyais.stream import UDPReceiver
from confluent_kafka import Producer
from pymongo import DESCENDING

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

myclient = pymongo.MongoClient("mongodb://mongodb:27017")
db = myclient["kafka_db"]
mycol_dynamic = db["ais_cyprus_dynamic"]
mycol_static = db["ais_cyprus_static"]
athens_ais = db['athens_ais']
bulgaria = db['bulgaria']
bulgaria_dynamic = db['bulgaria_dynamic']
bulgaria_static = db['bulgaria_static']
all_ais = db['all_ais']

date_min = datetime.strptime("08/04/2024 00:00:00", "%d/%m/%Y %H:%M:%S")
date_max = datetime.strptime("15/04/2024 00:00:00", "%d/%m/%Y %H:%M:%S")

results = mycol_dynamic.find({
    'timestamp': {
        '$gte': date_min,
        '$lte': date_max
    }
}).sort('time', DESCENDING)

for document in results:
    db.sample_dynamic_cyprus.insert_one(document)

different_format_timestamps = []

host = "0.0.0.0"
port = 9094

#for Athens if we want it again
# min_lat = 37.440604
# max_lat = 38.511865
# min_lon = 22.806318
# max_lon = 24.643915

min_lat = 42.031270
max_lat = 43.891879
min_lon = 27.028409
max_lon = 31.667294

ais = []

def delivery_report(err, msg):
    if err is not None:
        logging.error('Failed to deliver message: %s', err)
    else:
        logging.info('Message delivered to topic: %s', msg.topic())

while True:
    try:
        producer = Producer({'bootstrap.servers': 'kafka1:29092'})
        topic_metadata = producer.list_topics()
        topic_list = topic_metadata.topics
        for topic in topic_list:
            logging.info("----------------------------------------------- %s", topic)
        topic = 'ais_cyprus_dynamic'
        topic_static = 'ais_static'
        topic_bulgaria = 'ais_bulgaria_dynamic'
        
        for msg in UDPReceiver(host, port):

            decoded_b = msg.decode()
            message = decoded_b.asdict()
            ais = message
            
            if message is not None:
                message_type = message['msg_type']
                current_utc_time = datetime.utcnow()
                formatted_time = current_utc_time.strftime("%d/%m/%Y %H:%M:%S")

                new_data = {}
                new_data["timestamp"] = formatted_time
                
                if message_type in [1, 2, 3]:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["nav_status"] = message["status"]
                    new_data["longitude"] = message["lon"]
                    new_data["latitude"] = message["lat"]
                    new_data["heading"] = message["heading"]
                    new_data["sog"] = message["speed"]
                    new_data["cog"] = message["course"]
                    new_data["ais_type"] = message["msg_type"]

                    message = json.dumps(new_data)

                    if min_lat <= new_data["latitude"] <= max_lat and min_lon <= new_data["longitude"] <= max_lon:
                        producer.produce(topic_bulgaria, value=message.encode('utf-8'), callback=delivery_report)
                        producer.flush()
                        db.bulgaria.insert_one(new_data)
                    else:
                    
                        producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)
                        producer.flush()
                            
                        logging.info(f'new_data: {new_data}')

                        mycol_dynamic.insert_one(new_data)


                    
                elif message_type in [9]:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["nav_status"] = None
                    new_data["longitude"] = message["lon"]
                    new_data["latitude"] = message["lat"]
                    new_data["heading"] = None
                    new_data["sog"] = message["speed"]
                    new_data["cog"] = message["course"]
                    new_data["ais_type"] = message["msg_type"]

                    message = json.dumps(new_data)
                    
                    if min_lat <= new_data["latitude"] <= max_lat and min_lon <= new_data["longitude"] <= max_lon:
                        producer.produce(topic_bulgaria, value=message.encode('utf-8'), callback=delivery_report)
                        producer.flush()
                        db.bulgaria.insert_one(new_data)
                    else:

                        producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)
                        producer.flush()
    
                        db.ais_cyprus_dynamic.insert_one(new_data)
                    

                elif message_type in [18]:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["nav_status"] = None
                    new_data["longitude"] = message["lon"]
                    new_data["latitude"] = message["lat"]
                    new_data["heading"] = message["heading"]
                    new_data["sog"] = message["speed"]
                    new_data["cog"] = message["course"]
                    new_data["ais_type"] = message["msg_type"]
    
                    message = json.dumps(new_data)

                    if min_lat <= new_data["latitude"] <= max_lat and min_lon <= new_data["longitude"] <= max_lon:
                        producer.produce(topic_bulgaria, value=message.encode('utf-8'), callback=delivery_report)
                        producer.flush()
                        db.bulgaria.insert_one(new_data)
                        
                    else:
                        producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)
                        producer.flush()
    
                        db.ais_cyprus_dynamic.insert_one(new_data)

                        
                elif message_type == 5:
                    new_data["mmsi"] = message["mmsi"]
                    new_data["imo"] = message["imo"]
                    new_data["ship_name"] = message["shipname"]
                    new_data["call_sign"] = message["callsign"]
                    new_data["ship_type"] = message["ship_type"]
                    new_data["draught"] = message["draught"]
                    new_data["bow"] = message["to_bow"]
                    new_data["stern"] = message["to_stern"]
                    new_data["port"] = message["to_port"]
                    new_data["starboard"] = message["to_starboard"]
                    new_data["destination"] = message["destination"]
                    new_data["ais_type"] = message["msg_type"]

                    message = json.dumps(new_data)

                    producer.produce(topic_static, value=message.encode('utf-8'), callback=delivery_report)
                    producer.flush()
    
                    db.ais_cyprus_static.insert_one(new_data)


                elif message_type == 24 and "ship_type" in message:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["imo"] = None
                    new_data["ship_name"] = None
                    new_data["call_sign"] = message["callsign"]
                    new_data["ship_type"] = message["ship_type"]
                    new_data["draught"] = None
                    new_data["bow"] = message["to_bow"]
                    new_data["stern"] = message["to_stern"]
                    new_data["port"] = message["to_port"]
                    new_data["starboard"] = message["to_starboard"]
                    new_data["destination"] = None
                    new_data["ais_type"] = message["msg_type"]
                    
                    
                    message = json.dumps(new_data)

                    producer.produce(topic_static, value=message.encode('utf-8'), callback=delivery_report)
                    producer.flush()
    
                    db.ais_cyprus_static.insert_one(new_data)
                  

                elif message_type == 24 and "shipname" in message:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["imo"] = None
                    new_data["ship_name"] = message["shipname"]
                    new_data["call_sign"] = None
                    new_data["ship_type"] = None
                    new_data["draught"] = None
                    new_data["bow"] = None
                    new_data["stern"] = None
                    new_data["port"] = None
                    new_data["starboard"] = None
                    new_data["destination"] = None
                    new_data["ais_type"] = message["msg_type"]
                    
                    message = json.dumps(new_data)

                    producer.produce(topic_static, value=message.encode('utf-8'), callback=delivery_report)
                    producer.flush()
    
                    db.ais_cyprus_static.insert_one(new_data)                  
               
                    

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')
        logging.error(f'ais: {ais}')

    

