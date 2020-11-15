import time
import argparse
import requests
import paho.mqtt.client as mqtt
from flask import Flask, request

# TOPIC = 'MajaAndMarta/time'

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Serwis agregujacy dane</h1>
    sprawdź mnie :)
    '''


@app.route('/dane_pogodowe', methods=['POST'])
def dane_pogodowe():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    return 'thanks'


@app.route('/dane_temp', methods=['POST'])
def dane_temp():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    return 'thanks'


@app.route('/dane_z_licznika_pradu', methods=['POST'])
def dane_z_licznika_pradu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    return 'thanks'


@app.route('/dane_z_paneli', methods=['POST'])
def dane_z_paneli():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    return 'thanks'


@app.route('/ilosc_osob_w_domu', methods=['POST'])
def ilosc_osob_w_domu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    return 'thanks'



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=2323)
