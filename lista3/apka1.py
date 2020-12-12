import base
from datetime import datetime


def znajdz_dane(czas):
    # print(czas)
    for i in range(len(dane["observations"])):
        timestap = dane["observations"][i]["valid_time_gmt"]
        data = datetime.fromtimestamp(timestap)
        data_str = f"{data:%H:%M}"
        # print(data_str, czas)

        if data_str == czas:
            temperatura = konwersja_temp(dane["observations"][i]['temp'])
            cisnienie = round((dane["observations"][i]['pressure']) * 33.86389, 2)
            dane_wyjsciowe = {"Time": data_str, "Temp": temperatura, "Pres": cisnienie}
            return dane_wyjsciowe

    return None


def konwersja_temp(temp):
    return round((temp-32)/1.8, 2)


def zwroc_dane(czas):
    # print(dane)
    if czas[1] == 15:
        przed = znajdz_dane(base.godzina_na_str((czas[0], 0)))
        po = znajdz_dane(base.godzina_na_str((czas[0], 30)))
        temperatura = (przed["Temp"] + po["Temp"])/2
        cisnienie = ((przed["Pres"] + po["Pres"])/2)
        return {"Time:": base.godzina_na_str(czas), "Temp": temperatura, "Pres": cisnienie}

    elif czas[1] == 45:
        przed = znajdz_dane(base.godzina_na_str((czas[0], 30)))
        po = znajdz_dane(base.godzina_na_str((czas[0]+1, 0)))
        temperatura = (przed["Temp"] + po["Temp"])/2
        cisnienie = ((przed["Pres"] + po["Pres"])/2)
        return {"Time:": base.godzina_na_str(czas), "Temp": temperatura, "Pres": cisnienie}

    return znajdz_dane(base.godzina_na_str(czas))


if __name__ == '__main__':
    dane = base.importowanie_danych_json('Dane/dane_pogodowe.json')
    base.start_serwer(zwroc_dane, 'dane_pogodowe', 2321)
    # base.konfigurajcyjna(zwrocenie, 'dane_pogodowe')
