import logging
import json
import pymongo
from pykafka import KafkaClient
from datetime import datetime
from pyais import decode
from pyais.stream import UDPReceiver
from confluent_kafka import Producer

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
all_ais = db['all_ais']

different_format_timestamps = []

documents = db.ais_cyprus_dynamic.find()

# for doc in documents:
#     try:
#         formatted_timestamp = datetime.strptime(doc['timestamp'], '%m/%d/%Y %H:%M:%S')
#     except ValueError:
#         different_format_timestamps.append(doc['timestamp'])

# for timestamp in different_format_timestamps:
#     logging.info(f'timestamp: {timestamp}')

# kafka_client = KafkaClient(hosts='kafka1:29092')
# kafka_producer_dynamic = kafka_client.topics[b'ais_cyprus_dynamic'].get_producer()
# kafka_producer_static = kafka_client.topics[b'ais_cyprus_static'].get_producer()

host = "0.0.0.0"
port = 9094

min_lat = 37.440604
max_lat = 38.511865
min_lon = 22.806318
max_lon = 24.643915

# decoded_s = decode("!AIVDM,1,1,,A,137GAh001RR6v3TDS4HDdkb40D4h,0*35")
# as_dict = decoded_s.asdict()
# logging.info(f'as_dict: {as_dict}')
# decoded_s = as_dict['msg_type']
# logging.info(f'decoded_s: {decoded_s}')

# Create the Kafka producer
producer = Producer({
    'bootstrap.servers': 'kafka1:29092'
})
topic_metadata = producer.list_topics()
topic_list = topic_metadata.topics
for topic in topic_list:
    logging.info(f'topic: {topic}')
# topic = 'ais_cyprus_dynamic'

ais = []

def delivery_report(err, msg):
    if err is not None:
        logging.error('Failed to deliver message: %s', err)
    else:
        logging.info('Message delivered to topic: %s', msg.topic())

while True:
    try:
        
        for msg in UDPReceiver(host, port):
            # logging.info(f'msg: {msg}')
            decoded_b = msg.decode()
            # logging.info(f'decoded_s: {decoded_s}')
            # decoded_b = decode(msg)
            message = decoded_b.asdict()
            ais = message
            # logging.info(f'as_dict: {message}')
            # message = msg.decode()
            # logging.info(f'message: {decoded_b}')
            
            if message is not None:
                message_type = message['msg_type']
                # logging.info(f'message: {message}')
                
                # logging.info(f'message: {message_decoded}')
                
                current_utc_time = datetime.utcnow()
                formatted_time = current_utc_time.strftime("%d/%m/%Y %H:%M:%S")

                new_data = {}
                new_data["timestamp"] = formatted_time
                # logging.info(f'formatted_time: {formatted_time}')
                
                if message_type in [1, 2, 3]:
                    # logging.info(f'new_data: {new_data}')

                    new_data["mmsi"] = message["mmsi"]
                    new_data["nav_status"] = message["status"]
                    new_data["longitude"] = message["lon"]
                    new_data["latitude"] = message["lat"]
                    new_data["heading"] = message["heading"]
                    new_data["sog"] = message["speed"]
                    new_data["cog"] = message["course"]
                    new_data["ais_type"] = message["msg_type"]

                    # type_data = type(new_data)
                    # logging.info(f'type_data: {new_data}')
                    # message = json.dumps(new_data)
                    
                    # result = producer.produce(topic, value=message.encode('utf-8'), callback=delivery_report)
                    # producer.flush()

                    # logging.info(f'result: {result}')
                    mycol_dynamic.insert_one(new_data)

                    if min_lat <= new_data["latitude"] <= max_lat and min_lon <= new_data["longitude"] <= max_lon:
                        db.athens_ais.insert_one(new_data)
                    
                elif message_type in [9]:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["nav_status"] = None
                    new_data["longitude"] = message["lon"]
                    new_data["latitude"] = message["lat"]
                    new_data["heading"] = None
                    new_data["sog"] = message["speed"]
                    new_data["cog"] = message["course"]
                    new_data["ais_type"] = message["msg_type"]
    
                    db.ais_cyprus_dynamic.insert_one(new_data)

                    # message_json = json.dumps(message)
                    # message_bytes = message_json.encode('utf-8')
                    # kafka_producer_dynamic.produce(message_bytes)
                    
                    if min_lat <= new_data["latitude"] <= max_lat and min_lon <= new_data["longitude"] <= max_lon:
                        db.athens_ais.insert_one(new_data)

                elif message_type in [18]:

                    new_data["mmsi"] = message["mmsi"]
                    new_data["nav_status"] = None
                    new_data["longitude"] = message["lon"]
                    new_data["latitude"] = message["lat"]
                    new_data["heading"] = message["heading"]
                    new_data["sog"] = message["speed"]
                    new_data["cog"] = message["course"]
                    new_data["ais_type"] = message["msg_type"]
    
                    db.ais_cyprus_dynamic.insert_one(new_data)

                    # message_json = json.dumps(message)
                    # message_bytes = message_json.encode('utf-8')
                    # kafka_producer_dynamic.produce(message_bytes)
                    
                    if min_lat <= new_data["latitude"] <= max_lat and min_lon <= new_data["longitude"] <= max_lon:
                        db.athens_ais.insert_one(new_data)
                        
                elif message_type == 5:
                    # logging.info(f'as_dict: {message}')
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

                    db.ais_cyprus_static.insert_one(new_data)

                    # message_json = json.dumps(message)
                    # message_bytes = message_json.encode('utf-8')
                    # kafka_producer_static.produce(message_bytes)

                elif message_type == 24 and "ship_type" in message:

                    # logging.info(f'message: {message}')

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
                    
                    db.ais_cyprus_static.insert_one(new_data)

                    # message_json = json.dumps(message)
                    # message_bytes = message_json.encode('utf-8')
                    # kafka_producer_static.produce(message_bytes)
                    

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

                    logging.info(f'new_data: {new_data}')
                    
                    db.ais_cyprus_static.insert_one(new_data)

                    # message_json = json.dumps(message)
                    # message_bytes = message_json.encode('utf-8')
                    # kafka_producer_static.produce(message_bytes)
                    
               
                    

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')
        logging.error(f'ais: {ais}')

    

