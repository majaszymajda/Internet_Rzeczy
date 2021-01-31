import base


def zwroc_dane(czas):

    for i in range(1, 97):
        czas_z_danych = f'{str(czas[0]).rjust(2, "0")}:{str(czas[1]).rjust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"Time": dane[i][0], "Peoples": dane[i][1]}


if __name__ == '__main__':
    # base.wyslij_dane(zwroc_dane,'ilosc_osob_w_domu')
    dane = base.importowanie_danych_csv('Dane/ilosc_osob_w_domu.csv')
    base.start_serwer(zwroc_dane, 'ilosc_osob_w_domu', 2324)
