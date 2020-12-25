from flask import Flask, jsonify
from flask_mysql_connector import MySQL
from dop_python_pip_package.main_utils.math import add # our own pip library

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db' # this is the service name in docker compose
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE'] = 'test_db'

db = MySQL(app)

@app.route('/api/')
def home():
    # DB
    conn = db.connection
    cur = conn.cursor()
    cur.execute("select * from test;")
    output = cur.fetchall()

    # Proto

    # Pip package utils
    num = add(1, 2)
    
    return jsonify({"hello": str(output), "num": num})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
