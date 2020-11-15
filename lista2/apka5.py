import base
import requests
from datetime import datetime
import time


def zwroc_dane(czas):
    dane = base.importowanie_danych_json('Dane/dane_z_paneli.json')
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


if __name__ == '__main__':
    base.wyslij_dane(zwroc_dane)
