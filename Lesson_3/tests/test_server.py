import unittest
import sys
import os

sys.path.append(os.path.join(os.getcwd(), '..'))
from server import process_client_message as pcm
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR




class TestServer(unittest.TestCase):

    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    ok_dict = {
        RESPONSE: 200
    }


    def test_process_client_message_no_action(self):
        # Нет ключа ACTION в message
        self.assertEqual(pcm({TIME: 1.1, USER:{ACCOUNT_NAME: 'Guest'}}), self.err_dict)
    
    
    def test_process_client_message_wrong_action(self):
        # Неизвестное занчение ключа ACTION
        self.assertEqual(pcm({ACTION: 'Wrong', USER:{ACCOUNT_NAME: 'Guest'}}), self.err_dict)
    
    def test_process_client_message_no_time(self):
        # Нет ключа TIME в message
        self.assertEqual(pcm({ACTION: PRESENCE, USER:{ACCOUNT_NAME: 'Guest'}}), self.err_dict)
    
    
    def test_process_client_message_no_user(self):
        # Нет ключа USER в message
        self.assertEqual(pcm({ACTION: PRESENCE, TIME: 1.1}), self.err_dict)
    
    
    def test_process_client_message_unknow_user(self):
        # Неизвестное занчение ключа USER[ACCOUNT_NAME]
        self.assertEqual(pcm({ACTION: PRESENCE, TIME: 1.1, USER:{ACCOUNT_NAME: 'Guest1'}}), self.err_dict)
    
    
    def test_process_client_message_ok_check(self):
        # Корректный запрос
        self.assertEqual(pcm({ACTION: PRESENCE, TIME: 1.1, USER:{ACCOUNT_NAME: 'Guest'}}), self.ok_dict)



if __name__ == '__main__':
    unittest.main()



"""
Output:

......
----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
"""