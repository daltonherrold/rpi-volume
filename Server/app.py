#!C:\Users\snype_000\AppData\Local\Programs\Python\Python36-32\python.exe
from flask import Flask, jsonify, request
from utils import (get_applications,
                   increment_application_volume,
                   decrement_application_volume)

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello, World!"


@app.route('/get_all_volume', methods=['GET'])
def get_all_volume():
    return jsonify({'processes': get_applications()})


@app.route('/increment_process_volume', methods=['POST'])
def increment():
    process = request.form.get("process")
    print(process)
    return jsonify(increment_application_volume(process))


@app.route('/decrement_process_volume', methods=['POST'])
def decrement():
    process = request.form.get("process")
    return jsonify(decrement_application_volume(process))


if __name__ == '__main__':
    app.run(threaded=False, host='0.0.0.0')
