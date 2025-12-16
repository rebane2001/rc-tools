#!/usr/bin/python3
"""
rc-tools - flask basic example
==============================

note: flask automatically serves files in a ./static/ folder

Get data from a (usually) POST request:
request.data - as string
request.args - url params
request.form
request.files
request.values - args + form
request.json

note: use request.get_json(force=True) to ignore mime

"""
from flask import Flask, Response, send_file, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return f"index"

# http://127.0.0.1:8000/hi?name=lyra
@app.route('/hi')
def hi():
    return f"hi, {request.args.get('name')}!"

@app.route('/lyra.png')
def file():
    return send_file("lyra.png")

@app.route('/data', methods=['POST'])
def post():
    data = request.get_json(force=True)
    return jsonify(data)

@app.route('/headers')
def headers():
    resp = Response("CORS example")
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
