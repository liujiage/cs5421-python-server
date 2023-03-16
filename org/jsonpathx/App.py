from flask import Flask, request
from helper import json_xpath

app = Flask(__name__)

@app.route('/')
def index():
    return 'Web App with Python Flask!'

@app.route('/query', methods=['POST'])
def query():
    req = request.get_json()
    try:
        source = req.get('source')
        query = req.get('query')
        return {'success': 1, 'data': {'result': json_xpath(source, query)}}
    except:
        return {'success': 0, 'data': {}}


app.run(host='0.0.0.0', port=81)
