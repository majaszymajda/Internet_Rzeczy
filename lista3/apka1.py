import base
from datetime import datetime
from flask import Flask, request
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

dane = None

# lista_czestotliwosci = [15, 30, 45, 60]

@app.route('/')
def index():
    return f'''
    <h1>aplikacja pierwsza </h1>
    sprawdź mnie :)
    '''


# @app.route('/znajdz_dane')
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


@app.route('/zwroc_dane')
def zwrocenie():
    czas = base.godzina()
    dane = zwroc_dane(czas)
    return dane


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


@app.route("/zmiana")
def zmiana_interwalu():
    freq_arg = request.args.get('freq')
    try:
        freq = int(freq_arg)
    except ValueError:
        return f'Nie ma takiej dostępnej częstotliwości: {freq_arg}', 400

    if freq < 0:
        return f'czestotliwość powinna być wieksza od zera', 400

    scheduler.modify_job('dodawanie_danych', trigger='interval', seconds=freq)
    return 'ok'


if __name__ == '__main__':
    dane = base.importowanie_danych_json('Dane/dane_pogodowe.json')
    # base.wyslij_dane(zwroc_dane, 'dane_pogodowe')
    scheduler.add_job(id='dodawanie_danych', func=zwrocenie, trigger='interval', seconds=5)
    scheduler.start()
    app.run(host='0.0.0.0', port=2321)
