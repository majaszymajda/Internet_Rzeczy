import csv
import argparse
import requests
import paho.mqtt.client as mqtt
from flask import Flask, request, render_template

app = Flask(__name__)


dane_pogodowe_tab = []
dane_temp_tab = []
dane_z_licznika_pradu_tab = []
dane_z_paneli_tab = []
dane_ilosci_osob_w_domu_tab = []
czy_grzeje = False
czy_otwarte = False
temperatura = 0
temp_pola = 0
czy_zmiana = False
czy_zmiana_2 = False
czy_zapisuje = 0


temat1 = 'MajaiMarta/dane_pogodowe'
temat2 = 'MajaiMarta/dane_temp'
temat3 = 'MajaiMarta/dane_z_licznika_pradu'
temat4 = 'MajaiMarta/dane_z_paneli'
temat5 = 'MajaiMarta/ilosc_osob_w_domu'


@app.route('/')
def index():
    zbior_danych = {
        "sensory": {
            "sensor_pogodowy": dane_pogodowe_tab,
            "sensor_temperatury": dane_temp_tab,
            "sensor_z_licznika_pradu": dane_z_licznika_pradu_tab,
            "sensor_z paneli": dane_z_paneli_tab,
            "sensor_ilosci_osob": dane_ilosci_osob_w_domu_tab
            },
        "srednie": {
            "srednia_temperaturowa_powietrza": oblicz_srednia(dane_pogodowe_tab, "Temp"),
            "srednia_temperatury_w_domu": oblicz_srednia(dane_temp_tab, "Temp"),
            "srednia_zuzycia_pradu": oblicz_srednia(dane_z_licznika_pradu_tab, "Used"),
            "srednia_produkcji": oblicz_srednia(dane_z_paneli_tab, "Power"),
            "srednia_ludzi": oblicz_srednia(dane_ilosci_osob_w_domu_tab, "Peoples")
            }

        }
    return render_template('czwarta.html', zbior_danych=zbior_danych)
    # return render_template('aplikacja_webowa.html', zbior_danych=zbior_danych)


@app.route("/zapisywanie_danych")
def zapisywanie_danych(content, nazwa):
    global czy_zapisuje
    godzina_poczatkowa = request.args.get('time_start')
    godzina_koncowa = request.args.get('time_end')
    if godzina_poczatkowa == content["Time"]:
        czy_zapisuje = 1
    elif godzina_koncowa == content["Time"]:
        czy_zapisuje = 0
    while czy_zapisuje == 1:
        with open(f'{nazwa}.csv', 'w', encoding='utf-8') as csvfile:
            csvwrite = csv.writer(csvfile)
            csvwrite.writerow(content)
    return 'thx'


@app.route("/zmiana_interwalu")
def zmiana_interwalu():
    freq = request.args.get('freq')
    port = request.args.get('port')

    req = requests.get(url=f'http://0.0.0.0:{port}/zmiana?freq={freq}&port={port}')

    return req.text


@app.route('/grzejnik')
def grzejnik():
    global czy_grzeje
    czy_grzeje = not czy_grzeje
    if czy_grzeje is False:
        return 'grzejnik nie grzeje'
    return 'grzejnik grzeje'


@app.route('/okno')
def okno():
    global czy_otwarte
    czy_otwarte = not czy_otwarte
    if czy_otwarte is False:
        return 'okno zostało zamkniete'
    return 'okno zostało otwarte'


def oblicz_srednia(tablica, klucz):
    if len(tablica) == 0:
        print("brak danych")
        return None
    suma = sum([float(d[klucz]) for d in tablica])
    # print(sum/dzielnik)
    return round(suma/len(tablica), 2)


@app.route('/dane_pogodowe', methods=['POST'])
def dane_pogodowe():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    # print(content)
    dane_pogodowe_tab.append(content)

    # print(f'srednia temperaturowa: {oblicz_srednia(dane_pogodowe_tab, "Temp")}')
    # print(f'srednia cisnienia: {oblicz_srednia(dane_pogodowe_tab, "Pres")}')
    return 'thanks'


@app.route('/dane_temp', methods=['POST'])
def dane_temp():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    # print(content)
    global czy_zmiana
    global temperatura
    if czy_grzeje == czy_zmiana:
        temperatura = 0
        czy_zmiana = czy_grzeje
    else:
        if czy_grzeje == 1:
            temperatura += 1
            if temperatura > 5:
                temperatura = 5
        else:
            temperatura -= 1

    global czy_zmiana_2
    global temp_pola
    if czy_otwarte == czy_zmiana_2:
        temp_pola = 0
        czy_zmiana_2 = czy_otwarte
    else:
        if czy_otwarte == 1:
            temp_pola += 1
        else:
            temp_pola -= 1

    # poniewaz jezeli grzejnik jest wlaczony to dodajemy temperature i zmniejszamy wilgotnosc
    # print(temperatura)
    content["Temp"] = round(float(content["Temp"]) + temperatura * czy_grzeje, 2)
    content["Hum"] = round(float(content["Hum"]) - 2 * czy_grzeje, 2)
    # print(temp_pola)
    # jezeli otworzymy okno temperatura spada o 6 stopni
    content["Temp"] = round(float(content["Temp"]) - temp_pola * czy_otwarte, 2)
    content["Hum"] = round(float(content["Hum"]) + 2 * czy_otwarte, 2)

    # sprawdzanie czy w domu panuje optymalna temperature
    if float(content["Temp"]) <= 21.0:
        print("Temperatura w domu jest za niska!")
        print('----------------------------------------------------------')
        if czy_otwarte == 1:
            okno()
            print("Okno zostało zamknięte.")
        else:
            if czy_grzeje == 1:
                print("Grzejnik już jest włączony")
            else:
                grzejnik()
                print('Grzejnik został włączony.')
    if float(content["Temp"]) > 26.0:
        print("Temperatura w domu jest za wysoka! ")
        print('--------------------------------------------------------')
        if czy_grzeje == 1:
            grzejnik()
            print('Grzejnik został wyłączony.')
        else:
            if czy_otwarte == 1:
                print("Okno jest juz otwarte")
            else:
                okno()
                print("Okno zostało otwarte.")

    dane_temp_tab.append(content)
    # print(f'srednia temperaturowa domu: {oblicz_srednia(dane_temp_tab, "Temp")}')
    # print(f'średnia wilgotnosc w domu : {oblicz_srednia(dane_temp_tab, "Hum")}')
    return 'thanks'


@app.route('/dane_z_licznika_pradu', methods=['POST'])
def dane_z_licznika_pradu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    # print(content)
    # przy wlaczeniu grzejnika wzrasta zuzycie pradu
    content["Used"] = float(content["Used"]) + 0.300 * czy_grzeje
    dane_z_licznika_pradu_tab.append(content)
    # print(f'srednia zuzycie pradu: {oblicz_srednia(dane_z_licznika_pradu_tab, "Used")}')
    # print(f'srednia oddanego pradu: {oblicz_srednia( dane_z_licznika_pradu_tab, "Produced")}')

    return 'thanks'


@app.route('/dane_z_paneli', methods=['POST'])
def dane_z_paneli():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    # print(content)
    dane_z_paneli_tab.append(content)
    # print(f'srednia produkcja pradu: {oblicz_srednia(dane_z_paneli_tab, "Power")}')
    return 'thanks'


@app.route('/ilosc_osob_w_domu', methods=['POST'])
def ilosc_osob_w_domu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    # print(content)
    dane_ilosci_osob_w_domu_tab.append(content)
    #   print(f'srednia ilosc osob w domu: {oblicz_srednia( dane_ilosci_osob_w_domu_tab, "Peoples")}')

    return 'thanks'


#   METODA MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT with result code {str(rc)}")
    client.subscribe(temat1)
    client.subscribe(temat2)
    client.subscribe(temat3)
    client.subscribe(temat4)
    client.subscribe(temat5)


def on_message(client, userdata, msg):
    if msg.payload is not None:
        if str(msg.payload).find("Hum") is not None:
            content = dict(msg.payload)
            dane_temp_tab.append(content)
            oblicz_srednia(czestotliowsc, dane_temp_tab, "Hum")
            # print(dane_temp_tab)
        if str(msg.payload).find("Pres") is not None:
            dane_pogodowe_tab.append(msg.payload)
        if str(msg.payload).find("Produced") is not None:
            dane_z_licznika_pradu_tab.append(msg.payload)
        if str(msg.payload).find("Peoples") is not None:
            dane_ilosci_osob_w_domu_tab.append(msg.payload)
        if str(msg.payload).find("Power") is not None:
            dane_z_paneli_tab.append(msg.payload)
        print(int(msg.payload))


def mqtt_metoda():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect("test.mosquitto.org", 1883, 60)

    mqtt_client.loop_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metoda', default='HTTP', type=str, choices=['MQTT', 'HTTP'], help='metoda odbierania danych')
    parser.add_argument('-c', '--czestotliowsc', default=15, type=int, choices=[15, 30, 60], help='czestotliowsc agregowania danych [min]')

    args = parser.parse_args()
    czestotliowsc = args.czestotliowsc

    if args.metoda == "HTTP":
        app.run(host='0.0.0.0', port=2326)
    else:
        mqtt_metoda()
