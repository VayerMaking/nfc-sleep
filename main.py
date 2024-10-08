import datetime
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
import pytz

app = Flask(__name__)
state = TinyDB('state.json')
sleep_data = TinyDB('sleep.json')

@app.route('/init')
def init():
    # check if state.json and sleep.json files exist, if not create them
    try:
        state.all()[0]
    except IndexError:
        open("state.json", 'a').close()

    try:
        sleep_data.all()[0]
    except IndexError:
        open("sleep.json", 'a').close()

@app.route('/state')
def sleep():

    try:
        current_state = state.all()[0]
    except IndexError:
        state.insert({'isSleeping': False})
        current_state = state.all()[0]

    state.update({'isSleeping': not current_state['isSleeping']}, Query().isSleeping == current_state['isSleeping'])
    return current_state

@app.route('/sleep', methods=['POST', 'DELETE'])
def start():

    try:
        sleep_data.get(doc_id=1)
    except IndexError:
        sleep_data.insert({'start': None})

    if request.method == 'POST':
        current_time = datetime.datetime.now(pytz.timezone('Europe/Sofia')).timestamp()
        sleep_data.update({'start': current_time})
        return 'started'
    elif request.method == 'DELETE':
        timestamp = sleep_data.all()[0]['start']
        return jsonify({'start': datetime.datetime.fromtimestamp(timestamp, pytz.timezone('Europe/Sofia')).strftime('%Y-%m-%d %H:%M:%S')})
