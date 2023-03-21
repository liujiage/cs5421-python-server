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

    def test_wildcard(self):
        xpath = 'movies/*'
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = '*'
        res = json_xpath(json_data, xpath)
        print(res)


    def test_function(self):

        json_data = load_josn_by_file("../resources/movies.json")
        xpath = 'max(movies/year)'
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = 'min(movies/year)'
        res = json_xpath(json_data, xpath)
        print(res)

    def test_range_query(self):

        json_data = load_josn_by_file("../resources/movies.json")
        xpath = 'movies#0/title#1:3'
        res = json_xpath(json_data, xpath)
        print(res)

        # no start
        xpath = 'movies#0/title#:3'
        res = json_xpath(json_data, xpath)
        print(res)

        # no end
        xpath = 'movies#0/title#3:'
        res = json_xpath(json_data, xpath)
        print(res)

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

    def test_filter_list(self):
        xpath = "movies[cast HAS John Travolta]"
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = "movies[cast NOTHAS John Travolta]"
        res = json_xpath(json_data, xpath)
        print(res)

    def test_index_list(self):
        xpath = "movies#0/cast#0:2/#0"
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = "movies#0/cast#0/#0"
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

    def test_range_list(self):
        xpath = "movies#0/cast#0:2/#1:3"
        json_data = load_josn_by_file("../resources/movies.json")
        res = json_xpath(json_data, xpath)
        print(res)

    def test_movies2_key(self):
        xpath = 'movies/parent/cast'
        json_data = load_josn_by_file("../resources/movies2.json")
        res = json_xpath(json_data, xpath)
        print(res)


    def test_movies2_index(self):

        json_data = load_josn_by_file("../resources/movies2.json")
        xpath = 'movies#0/parent#0/cast#0/#2'
        res = json_xpath(json_data, xpath)
        print(res)

    def test_movies2_range(self):
        xpath = 'movies#0/parent#0/cast#0/#1:3'
        json_data = load_josn_by_file("../resources/movies2.json")
        res = json_xpath(json_data, xpath)
        print(res)

    def test_movies2_filter_list(self):
        xpath = "movies/parent[cast HAS Harvey Keitel]"
        json_data = load_josn_by_file("../resources/movies2.json")
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = "movies/parent[cast NOTHAS Harvey Keitel]"
        res = json_xpath(json_data, xpath)
        print(res)

    def test_movies2_recursive_descent(self):

        json_data = load_josn_by_file("../resources/movies2.json")

        xpath = "..cast"
        res = json_xpath(json_data, xpath)
        print(res)

        xpath = "..parent"
        res = json_xpath(json_data, xpath)
        print(res)






if __name__ == '__main__':
    unittest.main()
