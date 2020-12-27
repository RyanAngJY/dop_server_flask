import json
import os
from kafka import KafkaConsumer

import logging

logging.basicConfig(filename='consumer.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.warning('This will get logged to a file')

consumer = KafkaConsumer(
    "testtopic",
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

if __name__ == '__main__':
    logging.info("HELLO")
    for message in consumer:
        logging.info(message)

    logging.info("FINISH")
