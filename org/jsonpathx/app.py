from flask import Flask, request
from helper import json_xpath, visualize, jsonx_path_lalr
import json
import codecs

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
        # res = json_xpath(json.loads(source), query)
        res = jsonx_path_lalr(json.loads(source), query)
        if res[0] != None and res != "Error occurs":
            return {
                'error': 0,
                'error_msg': '', 
                'data': res
            }
        else:
            return {
                'error': 0,
                'error_msg': '', 
                'data': None
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
        source = json.loads(source)
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
    syntax = [
        {
            'id': 1,
            'expression': "$",
            'example': '$',
            'description': 'Select the root object'
        },
        {
            'id': 2,
            'expression': '.property',
            'example': '$.movie',
            'description': 'Select the child object'
        },
        {
            'id': 3,
            'expression': '["property"]',
            'example': '$["movie"]',
            'description': 'Select the child object'
        },
        {
            'id': 4,
            'expression': '*',
            'example': '$.[*]',
            'description': 'Select all fields of an element'
        },
        {
            'id': 5,
            'expression': '..property',
            'example': '$["movie"]..year',
            'description': 'Select all values of the given property in the structure.'
        },
        {   
            'id': 6,
            'expression': '[index]',
            'example': '$["movie"][0]',
            'description': 'Select the child element at index.'
        },
        {
            'id': 7,
            'expression': '[index, index]',
            'example': '$["movie"][0,1,2]',
            'description': 'Select the child elements at indexes.'
        },
        {
            'id': 8,
            'expression': '[start:end]',
            'example': '$["movie"][0:2]',
            'description': 'Similar to Python list slicing syntax. Return child elements at positions start through end.'
        },
        {
            'id': 9,
            'expression': '@',
            'example': '$["movie"][?(@.year>1997)]',
            'description': 'Reference to current object in filtering expressions.'
        },
        {
            'id': 10,
            'expression': '?',
            'example': '$["movie"][?(@.year>1997)]',
            'description': 'Apply a filter to selected element.'
        },
        {
            'id': 11,
            'expression': '==',
            'example': '$["movie"][?(@.year==1997)]',
            'description': 'Equal'
        },
        {
            'id': 12,
            'expression': '!=',
            'example': '$["movie"][?(@.year!=1997)]',
            'description': 'Not equal'
        },
        {
            'id': 13,
            'expression': '<',
            'example': '$["movie"][?(@.year<1997)]',
            'description': 'Less than'
        },
        {
            'id': 14,
            'expression': '<=',
            'example': '$["movie"][?(@.year>1997)]',
            'description': 'Not greater than'
        },
        {
            'id': 15,
            'expression': '>',
            'example': '$["movie"][?(@.year>1997)]',
            'description': 'Greater than'
        },
        {
            'id': 16,
            'expression': '>=',
            'example': '$["movie"][?(@.year>=1997)]',
            'description': 'Not less than'
        }
    ]
    return {
        'error': 0,
        'error_msg': '',
        'data': syntax
    }
    
app.run(host='127.0.0.1', port=81)
