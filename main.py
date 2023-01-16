from flask import Flask
from tinydb import TinyDB, Query

app = Flask(__name__)
state = TinyDB('state.json')

@app.route('/sleep')
def sleep():
    current_state = state.all()[0]
    state.update({'isSleeping': not current_state['isSleeping']}, Query().isSleeping == current_state['isSleeping'])
    return current_state
