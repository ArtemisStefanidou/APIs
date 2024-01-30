from pyais.stream import UDPStream
import logging
import json
import pymongo
from pykafka import KafkaClient

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
mycol_other = db["ais_cyprus_other"]

# mycol_static.drop()
# mycol_dynamic.drop()

kafka_client = KafkaClient(hosts='kafka1:29092')
kafka_producer_dynamic = kafka_client.topics[b'ais_cyprus_dynamic'].get_producer()
kafka_producer_static = kafka_client.topics[b'ais_cyprus_static'].get_producer()

host = "0.0.0.0"
port = 9094

while True:
    try:
        for msg in UDPStream(host, port):
            message = msg.decode()

            if message is not None:
                message_json = message.to_json()

                message_data = json.loads(message_json)
                message_type = message_data['decoded']['type']

                message_decoded = message_data['decoded']
                logging.info(f'message: {message_decoded}')

                if message_type in [1, 2, 3, 18, 9]:

                    message_decoded["sog"] = message_decoded.pop("speed", None)
                    message_decoded["cog"] = message_decoded.pop("course", None)
    
                    db.ais_cyprus_dynamic.insert_one(message_decoded)
                    
                    kafka_producer_dynamic.produce(message_decoded)

                elif message_type in [5, 24]:
                    
                    db.ais_cyprus_static.insert_one(message_decoded)
                    
                    kafka_producer_static.produce(message_decoded)

                else:
                    
                    db.other.insert_one(message_decoded)

    except Exception as e:
        logging.error(f'UDP stream failure: {e}')

    

