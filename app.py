import grpc
import json
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_mysql_connector import MySQL
from dop_python_pip_package.main_utils.math import add # our own pip library
from proto.dep.microservice import microservice_pb2_grpc, microservice_pb2
from kafka import KafkaProducer
from log_util import log, create_file_handler, default_formatter
from flask_socketio import SocketIO, emit

# Env variables
LOCALHOST = os.getenv("LOCALHOST", "localhost")
GRPC_HOST = os.getenv("GRPC_HOST", "localhost")
KAFKA_HOST = os.getenv("KAFKA_HOST", "localhost")
MYSQL_HOST = os.getenv("MYSQL_HOST", "db")  # this is the service name in docker compose
MYSQL_USER = os.getenv("MYSQL_USER", "root") # admin
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")  # dopdatabaseroot
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "test_db")

# Setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

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
    log("HOME")
    # Pip package utils
    num = add(1, 2)

    # DB
    log("GETTING FROM DB")
    output = "dummy_db_output"
    try:
        conn = db.connection
        cur = conn.cursor()
        cur.execute("select * from test limit 1;")
        output = cur.fetchall()
    except Exception as e:
        log("ERROR DB")
        log(e)    
        pass

    # Proto
    log("CALLING MICROSERVICE")
    channel = grpc.insecure_channel('{}:50051'.format(GRPC_HOST))
    stub = microservice_pb2_grpc.BlogServiceStub(channel)
    response = stub.GetBlog(microservice_pb2.GetBlogRequest())

    # Kafka
    log("SENDING TO KAFKA")
    future = producer.send(TOPIC, {"test": "hello"}).add_callback(on_send_success).add_errback(on_send_error)
    result = future.get(timeout=5)
    log("Result = {}".format(result))

    return jsonify({"db": str(output), "topic": result.topic, "lib": num, "microservice": str(response.blog)})


def on_send_success(metadata):
    log("SUCCESSFULLY SENT TO KAFKA")

def on_send_error(excp):
    log("ERROR AFTER SENT TO KAFKA")

@app.route('/api/produce/')
def produce():
    future = producer.send(TOPIC, {"test": "hello"}).add_callback(on_send_success).add_errback(on_send_error)
    result = future.get(timeout=5)
    return {}

# Handle the Client connecting to the websocket
@socketio.on('connect')
def test_connect():
    emit('myCustomResponseMessage', {'data': 'triggered test_connect'})

@socketio.on('message')
def handle_message(data):
    emit('myCustomResponseMessage', {'data': 'triggered handle_message'})

# Client socket has to connect to the correct namespace
@socketio.on('message', namespace="/custom_namespace")
def handle_namespace_message(data):
    # When we set broadcast=True, all socket clients connected to this namespace will receive a message with event name "broadcastedMessage"
    emit('broadcastedMessage', {'data': 'triggered broadcast handle_namespace_message'}, broadcast=True)
    # Note that if we do not set broadcast=True, the mesage will only be emitted to only the client socket
    emit('myCustomResponseMessage', {'data': 'triggered handle_namespace_message'})

# Will be triggered for messages with event name "custom_message"
@socketio.on('custom_message')
def handle_custom_message(data):
    emit('myCustomResponseMessage', {'data': 'triggered handle_custom_message'})

@app.route('/api/upload_image/', methods=["POST"])
@cross_origin()
def upload_image():
    print("UPLOADDD")
    # print(request.files['file'])
    return jsonify({
        "image_url": "image_url_here"
    })

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)
