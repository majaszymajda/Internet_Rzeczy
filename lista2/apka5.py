import base
import requests
from datetime import datetime
import time


def zwroc_dane(czas):
    moc = 0
    dane = base.importowanie_danych_json('Dane/dane_z_paneli.json')
    for panel in dane["manyData"]:
        for czas_iter in dane["manyData"][panel]:
            godzina = czas_iter.split()[1]
            # print(godzina)
            if godzina == base.godzina_na_str(czas):
                moc += dane["manyData"][panel][czas_iter][5]

    # print(czas, moc)
    return {'Time': base.godzina_na_str(czas), "Power": moc}


if __name__ == '__main__':
    base.wyslij_dane(zwroc_dane)
