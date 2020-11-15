import requests
import base
import time


def zwroc_dane(czas):
    dane = base.importowanie_danych_csv('Dane/dane_temp.csv')
    for i in range(1, 97):
        czas_z_danych = f'{czas[0]}:{str(czas[1]).ljust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"TIME": dane[i][0], "Temp": dane[i][1], "Hum": dane[i][2]}


if __name__ == '__main__':
    base.wyslij_dane(zwroc_dane)



