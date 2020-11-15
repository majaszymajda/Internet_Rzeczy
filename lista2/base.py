import argparse
import csv
import json
import requests
import time


def importowanie_danych_json(nazwa_pliku):
    with open(nazwa_pliku) as plik:

        try:
            dane = json.load(plik)
            #print(dane)

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
    parser.add_argument('-m', '--metoda', default='MQTT', type=str, choices=['MQTT', 'HTTP'], help='metoda wysylania danych')
    # parser.add_argument('-a', '--adres', required=True, type=str, help='wskazanie miejsca docelowego dla przesylania danych')
    parser.add_argument('-c', '--czestotliwosc', default=15, type=int, choices=[15, 30, 60], help='czestotliwosc wysylania danych [h]')

    args = parser.parse_args()
    return(args)


def godzina():
    # funkcja przyspiesza czas 60 krotnie
    t = time.time()
    tick = int(round(t // 15) % 96)
    return ((tick // 4, (tick % 4) * 15))


def on_connect(client, userdata, flags, rc):
    print("Połączenie udane!\nSprawdaj wyniki w konsoli apk_agregujaca.py")


def publish_value(client, topic, value):
    result = client.publish(topic=topic, payload=value)
    return result


def requests_post(url, data):
    result = requests.post(url, data=data)
    return result


def wyslij_dane(zwroc_dane):
    konfig = konfiguracja()
    czestotliwosc_funkcji = konfig.czestotliwosc
    metoda = konfig.metoda

    while (True):
        czas = godzina()
        print(zwroc_dane(czas))
        if metoda == "HTTP":
            pass  # requests.post(url=adres, json=dane)
        elif metoda == "MQTT":
            pass  # wyslij dane do brokera mqtt
        else:
            print("Nieznana metoda: {metoda}")
            exit(1)
        time.sleep(czestotliwosc_funkcji)

    return 0


if __name__ == "__main__":
    # while (True):
    #    print(godzina())
    #    time.sleep(5)

    # konfiguracja()

    importowanie_danych_csv('Dane/dane_temp.csv')
    # importowanie_danych_json('Dane/dane_pogodowe.json')
