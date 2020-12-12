import argparse
# import requests
import paho.mqtt.client as mqtt
from flask import Flask, request


app = Flask(__name__)


dane_pogodowe_tab = []
dane_temp_tab = []
dane_z_licznika_pradu_tab = []
dane_z_paneli_tab = []
dane_ilosci_osob_w_domu_tab = []
czestotliowsc = 60

temat1 = 'MajaiMarta/dane_pogodowe'
temat2 = 'MajaiMarta/dane_temp'
temat3 = 'MajaiMarta/dane_z_licznika_pradu'
temat4 = 'MajaiMarta/dane_z_paneli'
temat5 = 'MajaiMarta/ilosc_osob_w_domu'


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


def oblicz_srednia_MQTT(czestotliowsc, tablica, klucz):
    tablica2 = []
    for i in range(len(tablica)):
        tablica2.append(tablica[i].rsplit(",", ":"))
    print(tablica2)
    dzielnik = czestotliowsc//15
    if len(tablica) < dzielnik:
        print("za malo danych")
        return None
    sum = 0
    for j in range(dzielnik):

        sum += 1  # float(tablica2[-j-1][klucz])
    return sum/dzielnik


@app.route('/dane_pogodowe', methods=['POST'])
def dane_pogodowe():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_pogodowe_tab.append(content)
    print(f'srednia temperaturowa: {oblicz_srednia(czestotliowsc, dane_pogodowe_tab, "Temp")}')
    print(f'srednia cisnienia: {oblicz_srednia(czestotliowsc, dane_pogodowe_tab, "Pres")}')
    return 'thanks'


@app.route('/dane_temp', methods=['POST'])
def dane_temp():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_temp_tab.append(content)
    print(f'srednia temperaturowa domu: {oblicz_srednia(czestotliowsc, dane_temp_tab, "Temp")}')
    print(f'średnia wilgotnosc w domu : {oblicz_srednia(czestotliowsc, dane_temp_tab, "Hum")}')
    return 'thanks'


@app.route('/dane_z_licznika_pradu', methods=['POST'])
def dane_z_licznika_pradu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_z_licznika_pradu_tab.append(content)
    print(f'srednia zuzycie pradu: {oblicz_srednia(czestotliowsc, dane_z_licznika_pradu_tab, "Used")}')
    print(f'srednia oddanego pradu: {oblicz_srednia(czestotliowsc, dane_z_licznika_pradu_tab, "Produced")}')

    return 'thanks'


@app.route('/dane_z_paneli', methods=['POST'])
def dane_z_paneli():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_z_paneli_tab.append(content)
    print(f'srednia produkcja pradu: {oblicz_srednia(czestotliowsc, dane_z_paneli_tab, "Power")}')
    return 'thanks'


@app.route('/ilosc_osob_w_domu', methods=['POST'])
def ilosc_osob_w_domu():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    dane_ilosci_osob_w_domu_tab.append(content)
    print(f'srednia ilosc osob w domu: {oblicz_srednia(czestotliowsc, dane_ilosci_osob_w_domu_tab, "Peoples")}')

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
            dane_temp_tab.append(msg.payload)
            # oblicz_srednia_MQTT(czestotliowsc, dane_temp_tab, "Hum")
            # print(dane_temp_tab)
        if str(msg.payload).find("Pres") is not None:
            dane_pogodowe_tab.append(msg.payload)
        if str(msg.payload).find("Produced") is not None:
            dane_z_licznika_pradu_tab.append(msg.payload)
        if str(msg.payload).find("Peoples") is not None:
            dane_ilosci_osob_w_domu_tab.append(msg.payload)
        if str(msg.payload).find("Power") is not None:
            dane_z_paneli_tab.append(msg.payload)
        print(msg.payload)


def main():
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
        main()
