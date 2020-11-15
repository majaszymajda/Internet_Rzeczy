import requests
import base
import time


def zwroc_dane(czas):
    dane = base.importowanie_danych_csv('Dane/ilosc_osob_w_domu.csv')
    for i in range(1, 97):
        czas_z_danych = f'{czas[0]}:{str(czas[1]).ljust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"Time": dane[i][0], "Peoples": dane[i][1]}




if __name__ == '__main__':
    base.wyslij_dane(zwroc_dane,'ilosc_osob_w_domu')



