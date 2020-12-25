from flask import Flask, jsonify
from flask_mysql_connector import MySQL

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
    

    return jsonify({"hello": str(output)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
