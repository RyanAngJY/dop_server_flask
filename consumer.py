import json
import os
from kafka import KafkaConsumer

import logging

from log_util import create_file_and_std_out_logger

KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")

consumer_logger = create_file_and_std_out_logger("consumer_logger", "log/consumer.log", logging.INFO)

consumer = KafkaConsumer(
    "testtopic",
    bootstrap_servers=['{}:9092'.format(KAFKA_HOST)],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

if __name__ == '__main__':
    consumer_logger.info("START CONSUMER")
    for message in consumer:
        consumer_logger.info("RECEIVED MESSAGE FROM KAFKA: {}".format(message))

    consumer_logger.info("END CONSUMER")
