import grpc
import json
import os
from flask import Flask, jsonify
from flask_mysql_connector import MySQL
from dop_python_pip_package.main_utils.math import add # our own pip library
from proto.dep.microservice import microservice_pb2_grpc, microservice_pb2
from kafka import KafkaProducer

localhost = os.getenv("LOCALHOST", "localhost")

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db' # this is the service name in docker compose
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE'] = 'test_db'

db = MySQL(app)

producer = None

@app.route('/api/')
def home():
    # Pip package utils
    num = add(1, 2)

    # DB
    conn = db.connection
    cur = conn.cursor()
    cur.execute("select * from test;")
    output = cur.fetchall()

    # Proto
    # channel = grpc.insecure_channel('localhost:50051')
    channel = grpc.insecure_channel('{}:50051'.format(localhost))
    stub = microservice_pb2_grpc.BlogServiceStub(channel)
    response = stub.GetBlog(microservice_pb2.GetBlogRequest())

    return jsonify({"db": str(output), "lib": num, "microservice": str(response.blog)})

@app.route('/api/produce')
def produce():
    global producer
    if producer is None:
        producer = KafkaProducer(bootstrap_servers=['{}:9092'.format(localhost)],
                         value_serializer=lambda x: 
                         json.dumps(x).encode('utf-8'))
    producer.send('testtopic', value={"my_data": "hello"})
    return {}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
