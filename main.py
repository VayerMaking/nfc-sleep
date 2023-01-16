import datetime
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import pytz

app = Flask(__name__)
state = TinyDB('state.json')
sleep_data = TinyDB('sleep.json')

@app.route('/state')
def sleep():
    current_state = state.all()[0]
    state.update({'isSleeping': not current_state['isSleeping']}, Query().isSleeping == current_state['isSleeping'])
    return current_state

@app.route('/sleep', methods=['POST', 'DELETE'])
def start():
    if request.method == 'POST':
        current_time = datetime.datetime.now(pytz.utc).timestamp()
        sleep_data.update({'start': current_time})
        return 'started'
    elif request.method == 'DELETE':
        timestamp = sleep_data.all()[0]['start']
        return jsonify({'start': datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')})
