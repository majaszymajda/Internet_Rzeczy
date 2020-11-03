from flask import Flask, request
from datetime import datetime, timezone, timedelta

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Serwis czasowy</h1>
    sprawdź mnie :)
    '''


@app.route('/time')
def get_time():
    tz_arg = request.args.get('tz')
    try:
        tz = int(tz_arg)
    except ValueError:
        return f'Nie ma takiej strefy czasowej: {tz_arg}', 400

    if not -24 < tz < 24:
        return f'strefa czasowa powinna się zawierać w przedziale (-24, 24)', 400

    if tz >= 0:
        time = datetime.now(timezone(timedelta(hours=tz)))
    else:
        time = datetime.now(timezone(-timedelta(hours=tz)))
    return str(time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2323)
