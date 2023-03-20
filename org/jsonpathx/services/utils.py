import json

from jsonpath_ng.ext import parse

'''
load_josn_by_file
load json file to string
'''


def load_josn_by_file(file_path):
    with open(file_path) as json_content:
        return json.load(json_content)


'''
print_test
print out test log. Only for learn jsonpath-ng 
'''


def print_test(file_name, search_key_word):
    movies = load_josn_by_file(file_name)
    jsonpath_expression = parse(search_key_word)
    print("jsonpath_expression, type: {} value: {} ".format(type(jsonpath_expression), jsonpath_expression))
    for match in jsonpath_expression.find(movies):
        print("match.value: {}".format(match.value))

'''
get_value
return the value when value is empty then return def_value
'''

def get_value(v, def_value):
    if v:
        return v
    else:
        return def_value
