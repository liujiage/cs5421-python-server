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
        return {
            'error': 0,
            'error_msg': '', 
            'data': json_xpath(source, query)
        }
    except:
        return {
            'error': 1,
            'error_msg': 'Error', 
            'data': ''
        }

@app.route('/visual', methods=['POST'])
def visual():
    req = request.get_json()
    try:
        source = req.get('source')
        return {
            'error': 0,
            'error_msg': '', 
            'data': visual(source)
        }
    except:
        return {
            'error': 1,
            'error_msg': 'Error', 
            'data': ''
        }
    
app.run(host='0.0.0.0', port=81)
