import grpc
import json
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_mysql_connector import MySQL
from dop_python_pip_package.main_utils.math import add # our own pip library
from proto.dep.microservice import microservice_pb2_grpc, microservice_pb2
from kafka import KafkaProducer

# Env variables
LOCALHOST = os.getenv("LOCALHOST", "localhost")
GRPC_HOST = os.getenv("GRPC_HOST", "localhost")
KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")  # this is the service name in docker compose
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "test_db")

# Setup
app = Flask(__name__)
CORS(app)
log = app.logger

# MySQL Config
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DATABASE'] = MYSQL_DATABASE
db = MySQL(app)

# Kafka
TOPIC = "testtopic"
producer = KafkaProducer(
    bootstrap_servers=['{}:9092'.format(KAFKA_HOST)],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

@app.route('/api/')
def home():
    log.info("HOME")
    # Pip package utils
    num = add(1, 2)

    # DB
    conn = db.connection
    cur = conn.cursor()
    cur.execute("select * from test;")
    output = cur.fetchall()

    # Proto
    channel = grpc.insecure_channel('{}:50051'.format(GRPC_HOST))
    stub = microservice_pb2_grpc.BlogServiceStub(channel)
    response = stub.GetBlog(microservice_pb2.GetBlogRequest())

    # Kafka
    future = producer.send(TOPIC, {"test": "hello"}).add_callback(on_send_success).add_errback(on_send_error)
    result = future.get(timeout=5)

    return jsonify({"db": str(output), "lib": num, "microservice": str(response.blog)})


def on_send_success(metadata):
    print(metadata)

def on_send_error(excp):
    print(excp)

@app.route('/api/produce')
def produce():
    future = producer.send(TOPIC, {"test": "hello"}).add_callback(on_send_success).add_errback(on_send_error)
    result = future.get(timeout=5)
    return {}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
