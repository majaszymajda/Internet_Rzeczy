import base
from flask import Flask
from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()


@app.route('/')
def index():
    return '''
    <h1>aplikacja piata</h1>
    sprawdź mnie :)
    '''

@app.route('/zwroc_dane')
def zwrocenie():
    czas = base.godzina()
    dane = zwroc_dane(czas)
    return dane


def zwroc_dane(czas):
    moc = 0
    for panel in dane["manyData"]:
        for czas_iter in dane["manyData"][panel]:
            godzina = czas_iter.split()[1]
            # print(godzina)
            if godzina == base.godzina_na_str(czas):
                moc += dane["manyData"][panel][czas_iter][5]

    # print(czas, moc)
    return {'Time': base.godzina_na_str(czas), "Power": moc}


@app.route("/zmiana")
def zmiana_interwalu():
    nowy_interwal = 2
    scheduler.modify_job('dodawanie_danych',trigger='interval', seconds=nowy_interwal)
    return 'ok'

if __name__ == '__main__':
    # base.wyslij_dane(zwroc_dane, 'dane_z_paneli')
    dane = base.importowanie_danych_json('Dane/dane_z_paneli.json')
    scheduler.add_job(id='dodawanie_danych', func=zwrocenie, trigger='interval', seconds=5)
    scheduler.start()
    app.run(host='0.0.0.0', port=2325)