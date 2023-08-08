import sys
import logging
import traceback
import inspect

import logs.logs_configs.client_log_config
import logs.logs_configs.server_log_config




if sys.argv[0].find('server') == -1:
    LOGGER = logging.getLogger('client')
else:
    LOGGER = logging.getLogger('server')


def log(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        LOGGER.debug(f'Была вызвана функция {func.__name__} с параметрами: {args}, {kwargs} '
                     f'Вызов из модуля: {func.__module__} '
                     f'Вызов из функции: {traceback.format_stack()[0].strip().split()[-1]} '
                    #  f'Вызов из функции: {inspect.stack()[1][3]}'
                     , stacklevel=2)
        return res
    return wrapper



"""
Logs:

2023-06-28 00:40:38,142 DEBUG server.py 
Была вызвана функция process_client_message
с параметрами: ({'action': 'presence', 'time': 1687902038.1401205, 'user': {'account_name': 'Guest'}},), {}
Вызов из модуля: __main__
Вызов из функции: main()


2023-06-28 00:40:38,142 DEBUG client.py 
Была вызвана функция process_answer
с параметрами: ({'response': 200},), {}
Вызов из модуля: __main__
Вызов из функции: main()

"""