import requests
import base
import time


def zwroc_dane(czas):
    dane = base.importowanie_danych_csv('Dane/dane_z_licznika_pradu.csv')
    for i in range(1, 97):
        czas_z_danych = f'{czas[0]}:{str(czas[1]).ljust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"Time": dane[i][0], "Used": dane[i][1], "Produced": dane[i][2]}


def post_licznik_pradu():
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
    post_licznik_pradu()



