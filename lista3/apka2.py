import base


def zwroc_dane(czas):

    for i in range(1, 97):
        czas_z_danych = f'{str(czas[0]).rjust(2, "0")}:{str(czas[1]).rjust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"Time": dane[i][0], "Temp": dane[i][1], "Hum": dane[i][2]}
# dodać miejsce na grzejnik i okno


if __name__ == '__main__':
    dane = base.importowanie_danych_csv('Dane/dane_temp.csv')
    # base.wyslij_dane(zwroc_dane, 'dane_temp')
    base.start_serwer(zwroc_dane, 'dane_temp', 2322)
