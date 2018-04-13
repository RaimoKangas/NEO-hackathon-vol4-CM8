#
# Simple example how to expose data from python with Flask
#
# by Jussi
#
from flask import Flask

app = Flask(__name__)

@app.route('/')

def index():
    import json
    jsonData = '{"name": "Frank", "age": 39}'
    jsonToPython = json.loads(jsonData)
    return "JSON data: " + jsonData

if __name__ == '__main__':
    app.run(debug=True)

