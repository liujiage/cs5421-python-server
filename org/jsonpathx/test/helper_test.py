import unittest

from org.jsonpathx.helper import json_xpath
from org.jsonpathx.services.utils import load_josn_by_file


class MyTestCase(unittest.TestCase):

    def test_key_find_value_with_slash(self):
        xpath = 'movies/title'
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)


    # in this code, when using index to find, every elements on paths need an index
    def test_index(self):
        xpath = 'movies#0/title#0'
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = 'movies#0/year#1'
        res = json_xpath(json_data, xpath)
        print(res)


    # def test_function(self):
    #     xpath = 'movies/year'
    #     json_data = load_josn_by_file("../resources/movies.json")
    #     res = json_xpath(json_data, xpath)
    #     print(res)



    def test_filter(self):
        xpath = 'movies[director==Quentin Tarantino]'
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = 'movies[year==1994]'
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = 'movies[year>1994]'
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = 'movies[director!=Quentin Tarantino]'
        res = json_xpath(json_data, xpath)
        print(res)




if __name__ == '__main__':
    unittest.main()
