from typing import List, Dict
from flask import Flask, jsonify, request
import mysql.connector
import folium
import time

app = Flask(__name__)

def test_table():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'students'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM test_table')
    results = [{name: location} for (name, location) in cursor]
    cursor.close()
    connection.close()

    return results

@app.route('/')
def home():
    return "<h1>Welcome</h1><a href=./db>Click</a> to see the database!<br><a href=./map>Click</a> to see the world map!<br><a href=./form>Click</a> to add new student!"

@app.route('/db')
def see_db():
    results = test_table()
    time.sleep(2)
    return jsonify({'test_table': results})    

@app.route('/form')
def form():
    return """
        <form action="/data" method = "POST">
        <p>Name <input type = "text" name = "Name" /></p>
        <p>Coordinates (ex: 35.8592948,104.1361118) <input type = "text" name = "Coordinates" /></p>
        <p><input type = "submit" value = "Submit" /></p>
        </form>
    """
    
@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit data to database."
    if request.method == 'POST':
        form_data = request.form
        config = {
            'user': 'root',
            'password': 'root',
            'host': 'db',
            'port': '3306',
            'database': 'students'
        }
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        
        inputs = []
        for k,input in form_data.items():
            inputs.append(input)

        cursor.execute(f'INSERT INTO test_table (name, location) VALUES ("{inputs[0]}", "{inputs[1]}")')
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return home()

@app.route('/map/')
def map():
    start_coords = (36.752887, 3.042048)
    folium_map = folium.Map(location=start_coords, zoom_start=3)
    folium.TileLayer(tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', attr='&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, \
                 &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors').add_to(folium_map)
    for student in test_table():
        for name,location in student.items():
            latitude = float(location.split(',')[0])
            longitude = float(location.split(',')[1])
            folium.Marker(
                location=[latitude,longitude],
                popup=name,
            ).add_to(folium_map)
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(host='0.0.0.0')