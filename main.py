from flask import Flask

app = Flask(__name__)

global isSleeping
isSleeping = False

@app.route('/sleep')
def sleep():
    global isSleeping
    isSleeping = not isSleeping
    return str(not isSleeping)
