import unittest

from org.jsonpathx.services.utils import load_josn_by_file
from org.jsonpathx.services.parser import Parser


class MyTestCase(unittest.TestCase):
    '''
    json mapping dict
    .name mapping ['name']
    '''

    def test_demo1(self):
        keyword = "$.*.name"
        data = load_josn_by_file("../resources/purchase_order.json")
        print(data['billTo']['name'])
        tokens = keyword.split(".")
        print(tokens)
        keyword = "$.movies[?(@.cast[:] =~ 'De Niro')].*"
        tokens = keyword.split(".")
        print(tokens)

    def test_demo2(self):
        data = load_josn_by_file("../resources/movies.json")
        print(type(data['movies']))
        for d in data['movies']:  # the type is list
            print(type(d['cast']))
            for v in d['cast'][:]:  # # the type is list
                if v == 'Uma Thurman':
                    print(d['cast'][:])
                    break

    def test_demo3(self):
        data = load_josn_by_file("../resources/movies.json")
        letter = [x for x in data['movies'][0]['cast']]
        print(letter)

    def test_demo4(self):
        keyword = "movies[0].{parent.cast[:] =~ 'De Niro'}.title.parent.child[0].name"
        res = Parser().parse(keyword)
        print(res)

    def test_demo5(self):
        keyword = "movies[0].parent.{cast[:] =~ 'De Niro'}.title[:]"
        res = Parser().parse(keyword)
        print(res)

    def test_demo6(self):
        keyword = "cast[:] =~ 'De Niro'"
        res = Parser().parse(keyword)
        print(res)

if __name__ == '__main__':
    unittest.main()
