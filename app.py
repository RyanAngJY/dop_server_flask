import grpc
import json
import os
from flask import Flask, jsonify
from flask_mysql_connector import MySQL
from dop_python_pip_package.main_utils.math import add # our own pip library
from proto.dep.microservice import microservice_pb2_grpc, microservice_pb2
from kafka import KafkaProducer

LOCALHOST = os.getenv("LOCALHOST", "localhost")
TOPIC = "testtopic"

app = Flask(__name__)
log = app.logger

app.config['MYSQL_HOST'] = 'db' # this is the service name in docker compose
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE'] = 'test_db'

db = MySQL(app)

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
    # channel = grpc.insecure_channel('localhost:50051')
    channel = grpc.insecure_channel('{}:50051'.format(LOCALHOST))
    stub = microservice_pb2_grpc.BlogServiceStub(channel)
    response = stub.GetBlog(microservice_pb2.GetBlogRequest())

    return jsonify({"db": str(output), "lib": num, "microservice": str(response.blog)})

# Kafka
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def on_send_success(metadata):
    print(metadata)

def on_send_error(excp):
    print("ERR: ")
    print(excp)

@app.route('/api/produce')
def produce():
    print("HERE")
    future = producer.send(TOPIC, {"test": "hello"}).add_callback(on_send_success).add_errback(on_send_error)
    result = future.get(timeout=5)
    return {}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
