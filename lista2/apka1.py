import base
import requests
from datetime import datetime
import time


def zwroc_dane(czas):
    dane = base.importowanie_danych_json('Dane/dane_pogodowe.json')
    # print(dane)
    for i in range(len(dane["observations"])):
        czas_z_danych = f'{czas[0]}:{str(czas[1]).ljust(2, "0")}'
        timestap = dane["observations"][i]["valid_time_gmt"]
        data = datetime.fromtimestamp(timestap)
        data_str = f"{data: %H:%M}"
        print(data_str, czas_z_danych)
        if czas[1] == 15:
            
            temperatura = (dane["observations"][i]['temp'] - 32)/2
        if czas[1] == 45:


        if data_str == czas_z_danych:
            temperatura = (dane["observations"][i]['temp'] - 32)/2
            cisnienie = (dane["observations"][i]['pressure']) * 33.86389
            slownik = {"Time:": data_str, "Temp":temperatura, "Pres": cisnienie}
            return slownik




def post_temp_we_wroclawiu():
    # dane = importowanie_danych_csv('Dane/dane_temp.csv')
    konfig = base.konfiguracja()
    czestotliwosc_funkcji = konfig.czestotliwosc
    # adres = konfig.adres
    while (True):
        czas = base.godzina()
        print(zwroc_dane(czas))
        # requests.post(url = adres, json=dane)
        time.sleep(czestotliwosc_funkcji)

    return 0

if __name__ == '__main__':
    post_temp_we_wroclawiu()
