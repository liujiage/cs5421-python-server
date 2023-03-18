import unittest
from org.jsonpathx.services.utils import print_test

class MyTestCase(unittest.TestCase):
    def test_demo1(self):
        print_test("../resources/movies.json", "$.movies[?(@.cast[:] =~ 'De Niro')].title")

    def test_demo2(self):
        print_test("../resources/movies.json", "$.movies[*].title")

    def test_demo3(self):
        print_test("../resources/movies.json", "$.movies[0].title")

    def test_demo4(self):
        print_test("../resources/movies.json", "$..year")

    def test_demo5(self):
        print_test("../resources/movies.json", "$.movies[?(@.year < 1990)]")

    def test_demo6(self):
        print_test("../resources/movies.json", "$.movies[?(@.year < 1990)].title")

    def test_demo6(self):
        print_test("../resources/movies.json", "$.movies[0]")


if __name__ == '__main__':
    unittest.main()
