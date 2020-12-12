import argparse
import csv
import json
import requests
import time
import paho.mqtt.client as mqtt
from flask import Flask, request
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

topic = 'MajaiMarta'


def importowanie_danych_json(nazwa_pliku):
    with open(nazwa_pliku) as plik:

        try:
            dane = json.load(plik)
            # print(dane)

        except json.JSONDecodeError as error:
            print(f"nie udało się wczytać pliku {nazwa_pliku} błąd: {error.msg} ")
            return None

    return dane


def importowanie_danych_csv(nazwa_pliku):
    with open(nazwa_pliku) as plik:
        dane = csv.reader(plik, delimiter=';')
        dane_tablica = []
        try:
            for dana in dane:
                dane_tablica.append(dana)
            # print(dane_tablica)
        except csv.Error as error:
            print(f"nie udało się wczytać pliku {nazwa_pliku} błąd: {error.msg} ")
            return None

    return dane_tablica


def konfiguracja():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--metoda', default='HTTP', type=str, choices=['MQTT', 'HTTP'], help='metoda wysylania danych')
    parser.add_argument('-a', '--adres', default='0.0.0.0:2326', type=str, help='wskazanie miejsca docelowego dla przesylania danych')
    parser.add_argument('-c', '--czestotliwosc', default=15, type=int, choices=[15, 30, 60], help='czestotliwosc wysylania danych [h]')

    args = parser.parse_args()
    return(args)


def godzina():
    # funkcja przyspiesza czas 60 krotnie
    t = time.time()
    tick = int(round(t // 15) % 96)
    return ((tick // 4, (tick % 4) * 15))


def godzina_na_str(czas):
    return f'{str(czas[0]).rjust(2, "0")}:{str(czas[1]).rjust(2, "0")}'


@app.route("/zmiana")
def zmiana_interwalu():
    freq_arg = request.args.get('freq')
    try:
        freq = int(freq_arg)
    except ValueError:
        return f'Nie ma takiej dostępnej częstotliwości: {freq_arg}', 400

    if freq < 0:
        return f'czestotliwość powinna być wieksza od zera', 400

    scheduler.modify_job('dodawanie_danych', trigger='interval', seconds=freq)
    return 'ok'


@app.route("/wyslij_dane")
def wyslij_dane():
    # czestotliwosc_funkcji = konfig.czestotliwosc
    metoda = konfig.metoda
    adres = konfig.adres
    czas = godzina()
    dane = funkcja_zwracajaca_dane(czas)

    if metoda == "HTTP":
        requests.post(url=f'http://{adres}/{podana_sciezka}', json=dane)
    elif metoda == "MQTT":
        mqtt_client = mqtt.Client()
        mqtt_client.connect("test.mosquitto.org", 1883, 60)
        mqtt_client.publish(topic=f"{topic}/{podana_sciezka}", payload=str(dane))
    else:
        print(f"Nieznana metoda: {metoda}")
        exit(1)

    return 0


def start_serwer(zwroc_dane, sciezka, port_podany):
    global konfig
    konfig = konfiguracja()

    global podana_sciezka
    podana_sciezka = sciezka

    global funkcja_zwracajaca_dane
    funkcja_zwracajaca_dane = zwroc_dane

    scheduler.add_job(id='dodawanie_danych', func=wyslij_dane, trigger='interval', seconds=konfig.czestotliwosc)
    scheduler.start()
    app.run(host='0.0.0.0', port=port_podany)


if __name__ == "__main__":
    importowanie_danych_csv('Dane/dane_temp.csv')
