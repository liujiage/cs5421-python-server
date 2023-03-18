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

if __name__ == '__main__':
    unittest.main()
