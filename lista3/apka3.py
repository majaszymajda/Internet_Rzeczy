import base


def zwroc_dane(czas):
    for i in range(1, 97):
        czas_z_danych = f'{str(czas[0]).rjust(2, "0")}:{str(czas[1]).rjust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"Time": dane[i][0], "Used": dane[i][1], "Produced": dane[i][2]}


if __name__ == '__main__':
    # base.wyslij_dane(zwroc_dane, 'dane_z_licznika_pradu')
    dane = base.importowanie_danych_csv('Dane/dane_z_licznika_pradu.csv')
    base.start_serwer(zwroc_dane, 'dane_z_licznika_pradu', 2323)
