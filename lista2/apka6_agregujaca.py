import time
import argparse
import requests
import paho.mqtt.client as mqtt
from flask import Flask, request


# TOPIC = 'MajaAndMarta/time'

app = Flask(__name__)


dane_pogodowe_tab = []
dane_temp_tab = []
dane_z_licznika_pradu_tab = []
dane_z_paneli_tab = []
dane_ilosci_osob_w_domu_tab = []

@app.route('/')
def index():
    return '''
    <h1>Serwis agregujacy dane</h1>
    sprawdź mnie :)
    '''



def oblicz_srednia(czestotliowsc, tablica, klucz):
    dzielnik = czestotliowsc//15
    if len(tablica) < dzielnik:
        print("za malo danych")
        return None
    sum = 0
    for i in range(dzielnik):
        sum += float(tablica[-i-1][klucz])
    return sum/dzielnik



@app.route('/dane_pogodowe', methods=['POST'])
def dane_pogodowe():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_pogodowe_tab.append(content)
    print(f'srednia temperaturowa: {oblicz_srednia(60, dane_pogodowe_tab, "Temp")}')
    print(f'srednia cisnienia: {oblicz_srednia(60, dane_pogodowe_tab, "Pres")}')
    return 'thanks'


@app.route('/dane_temp', methods=['POST'])
def dane_temp():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_temp_tab.append(content)
    print(f'srednia temperaturowa domu: {oblicz_srednia(60, dane_temp_tab, "Temp")}')
    print(f'średnia wilgotnosc w domu : {oblicz_srednia(60, dane_temp_tab, "Hum")}')
    return 'thanks'


@app.route('/dane_z_licznika_pradu', methods=['POST'])
def dane_z_licznika_pradu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_z_licznika_pradu_tab.append(content)
    print(f'srednia zuzycie pradu: {oblicz_srednia(60, dane_z_licznika_pradu_tab, "Used")}')
    print(f'srednia oddanego pradu: {oblicz_srednia(60, dane_z_licznika_pradu_tab, "Produced")}')

    return 'thanks'


@app.route('/dane_z_paneli', methods=['POST'])
def dane_z_paneli():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_z_paneli_tab.append(content)
    print(f'srednia produkcja pradu: {oblicz_srednia(60, dane_z_paneli_tab, "Power")}')
    return 'thanks'


@app.route('/ilosc_osob_w_domu', methods=['POST'])
def ilosc_osob_w_domu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_ilosci_osob_w_domu_tab.append(content)
    print(f'srednia ilosc osob w domu: {oblicz_srednia(60, dane_ilosci_osob_w_domu_tab, "Peoples")}')

    return 'thanks'



if __name__ == "__main__":

    app.run(host='0.0.0.0', port=2323)
