import json
import unittest

from org.jsonpathx.helper import json_xpath


def load_josn_by_file(file_path):
    with open(file_path) as json_content:
        return json.load(json_content)

class MyTestCase(unittest.TestCase):
    def test_key_find_value(self):
        # Test case 1: Key query
        json_data = '{"name": "Bre", "age": 25}'
        xpath = 'name'
        res = json_xpath(json_data, xpath)
        print(res)
        json_data = load_josn_by_file("./resources/movies.json")
        print(json_data)
        res = json_xpath(json_data, xpath)
        print(res)

    def test_(self):
        json_data = '[{"people": [{"name": "Bre", "age": 25}, {"name": "Stephane", "age": 30}]}, {"people": [{"name": "Bre1", "age": 26}, {"name": "Stephane1", "age": 31}]}]'
        xpath = 'movies/title'
        json_data = load_josn_by_file("./resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

if __name__ == '__main__':
    unittest.main()
