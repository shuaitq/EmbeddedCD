from flask import Flask, Response, request
import Adafruit_DHT
import sqlite3
import json

app = Flask(__name__)

@app.route('/api/gettmp',methods=["GET", "POST"])
def draw_stone():
    d_hum,d_temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22,4)
    d_hum = round(d_hum,2)
    d_temp = round(d_temp,2)
    data = [d_temp,d_hum]
    return Response(json.dumps(data),  mimetype='application/json')

@app.route('/api/history', methods=["GET", "POST"])
def get_history():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    limit = 8640
    if request.args.get('limit') != None:
        limit = int(request.args.get('limit'))
    cursor.execute('select * from weather order by id desc limit ?', [limit])
    data = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return Response(json.dumps(data), mimetype='application/json')

@app.route('/')
def staff_page():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0',port=5005)
