from flask import Flask
from waitress import serve

app = Flask(__name__)

@app.route('/')
def hello():
    return "{'data':{['result':{[39, 34, 28, 33, 39, 36, 33, 31, 32, 33, 27, 27]}]}"

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080)
