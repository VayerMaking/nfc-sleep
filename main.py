from flask import Flask

app = Flask(__name__)

@app.route('/sleep')
def sleep():
    return "ok"