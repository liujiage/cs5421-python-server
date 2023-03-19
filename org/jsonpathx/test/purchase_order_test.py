import unittest

from org.jsonpathx.services.utils import print_test, load_josn_by_file


class MyTestCase(unittest.TestCase):
    def test_demo1(self):
        print_test("../resources/purchase_order.json", "$.billTo")

    def test_demo2(self):
        print_test("../resources/purchase_order.json", "billTo")

    def test_demo3(self):
        print_test("../resources/purchase_order.json", "billTo.name")


if __name__ == '__main__':
    unittest.main()
