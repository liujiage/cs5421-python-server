from flask import Flask, request
from helper import json_xpath, visualize

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
        data = visualize(source)
        return {
            'error': 0,
            'error_msg': '', 
            'data': data
        }
    except:
        return {
            'error': 1,
            'error_msg': 'Error', 
            'data': ''
        }
    
@app.route('/expressions', methods=['GET'])
def expressions():
    syntax = """parse keyword
input:  movies[0].parent.{cast[:] =~ 'De Niro'}.title[:]...
output: ['element:movies', 'slice:[0]', 'element:parent', "query:{cast[:] =~ 'De Niro'}", 'element:title', 'slice:[:]']...
_syntax_next = "."
_syntax_slice_left = "["
_syntax_slice_right = "]"
_syntax_query_left = "{"
_syntax_query_right = "}"
"""
    return {
        'error': 0,
        'error_msg': '',
        'data': syntax
    }
    
app.run(host='127.0.0.1', port=81)
