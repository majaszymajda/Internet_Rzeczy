import base
import schedule
from flask import Flask
from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()


@app.route('/')
def index():
    return '''
    <h1>aplikacja trzecia</h1>
    sprawdź mnie :)
    '''

@app.route('/zwroc_dane')
def zwrocenie():
    czas = base.godzina()
    dane = zwroc_dane(czas)
    return dane


def zwroc_dane(czas):
    dane = base.importowanie_danych_csv('Dane/dane_z_licznika_pradu.csv')
    for i in range(1, 97):
        czas_z_danych = f'{czas[0]}:{str(czas[1]).ljust(2, "0")}'
        if czas_z_danych == dane[i][0]:
            return {"Time": dane[i][0], "Used": dane[i][1], "Produced": dane[i][2]}


@app.route("/zmiana")
def zmiana_interwalu():
    nowy_interwal = 2
    scheduler.modify_job('dodawanie_danych',trigger='interval', seconds=nowy_interwal)
    return 'ok'


if __name__ == '__main__':
    # base.wyslij_dane(zwroc_dane, 'dane_z_licznika_pradu')
    scheduler.add_job(id='dodawanie_danych', func=zwrocenie, trigger='interval', seconds=5)
    scheduler.start()
    app.run(host='0.0.0.0', port=2323)
