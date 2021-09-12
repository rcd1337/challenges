from django.test import Client
import unittest, json
from .utilities.util import exception, isValid, isException, numToWord


class Tests(unittest.TestCase):

    # isValid tests
    def test_isValid_1(self):
        """ Check that '-015' is valid """
        self.assertTrue(isValid('-015'))

    def test_isValid_2(self):
        """ Check that '99999' is valid """
        self.assertTrue(isValid('99999'))

    def test_isValid_3(self):
        """ Check that '100000' is valid """
        self.assertFalse(isValid('100000'))


    # isException tests
    def test_isException_1(self):
        """ Check that 13 is an exception """
        self.assertTrue(isException(13))

    def test_isException_2(self):
        """ Check that 21 is not an exception """
        self.assertFalse(isException(21))

    def test_isException_3(self):
        """ Check that 9 is not an exception """
        self.assertFalse(isException(9))


    # exception tests
    def test_exception_1(self):
        """ Check that '0' returns "zero" """
        self.assertEquals(exception(0), 'zero')


    # numToWord test
    def test_numToWord_1(self):
        """ Check that '1337' returns "mil trezentos e trinta e sete """
        self.assertEquals(numToWord('1337'), 'mil e trezentos e trinta e sete')


    # test server
    def test_index_1(self):
        c = Client()
        response = c.get("/13")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'extenso': 'treze'}
        )

    def test_index_2(self):
        c = Client()
        response = c.get("/-1337")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {'extenso': 'menos mil e trezentos e trinta e sete'}
        )

    def test_index_3(self):
        c = Client()
        response = c.get("/1")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"extenso": "um"}
        )

    def test_index_4(self):
        c = Client()
        response = c.get("/-1042")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"extenso": "menos mil e quarenta e dois"}
        )

    def test_index_5(self):
        c = Client()
        response = c.get("/94587")
        self.assertEquals(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"extenso": "noventa e quatro mil e quinhentos e oitenta e sete"}
        )


if __name__ == "__main__":
    unittest.main()