import os
from flask import Flask, request
import uuid
import json

PATH = "responses"

app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <h1>Serwis czasowy vol2</h1>
    sprawdź mnie :)
    '''


@app.route('/one_more_time', methods=['POST'])
def one_more_time():
    if not request.is_json:
        return "it is not a json", 400

    content = request.get_json()
    print(content)
    name = f"resp_{uuid.uuid4()}.json"

    with open(f"{PATH}/{name}", 'w') as f:
        json.dump(content, f, indent=4)

    return 'thanks'


if __name__ == '__main__':
    if not os.path.isdir(PATH):
        os.mkdir(PATH)

    app.run(host='0.0.0.0', port=2121)
