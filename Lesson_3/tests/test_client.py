import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from client import create_presense, process_answer
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR



class TestClient(unittest.TestCase):
    def test_create_presense(self):
        # Тест корректного запроса
        test = create_presense()
        test[TIME] = 1.1

        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})


    def test_process_answer_200(self):
        # Тест корректного разбора ответа 200
        self.assertEqual(process_answer({RESPONSE: 200}), '200 : OK')
    
    
    def test_process_answer_400(self):
        # Тест корректного разбора ответа 400
        self.assertEqual(process_answer({RESPONSE: 400, ERROR: 'Bad request'}), '400 : Bad request')

    
    def test_process_answer_no_response(self):
        # Тест исключения без поля RESPONSE
        self.assertRaises(ValueError, process_answer, {ACTION: PRESENCE})




if __name__ == '__main__':
    unittest.main()




"""
Output:

....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
"""