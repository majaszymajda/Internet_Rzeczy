import time
import argparse
import requests
import paho.mqtt.client as mqtt
from flask import Flask, request

TOPIC = 'MajaAndMarta/time'

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Serwis agregujacy dane</h1>
    sprawdź mnie :)
    '''

@app.route('')

if __name__ == "__main__":
    main()