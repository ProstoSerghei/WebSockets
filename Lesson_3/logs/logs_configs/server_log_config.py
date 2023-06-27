import sys
import os
import logging
import logging.handlers

sys.path.append('../../')
from common.variables import LOGGING_LEVEL


# Определить формат сообщений
SERVER_FORMATTER = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовить путь
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(os.path.dirname(PATH), 'logs_files\server.log')

# Создать обработчик, который выводит сообщения с уровнем ERROR в поток stderr
STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)
LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding='utf-8', interval=1, when='midnight')
LOG_FILE.setFormatter(SERVER_FORMATTER)

# Создать регистратор
LOGGER = logging.getLogger('server')
LOGGER.addHandler(STREAM_HANDLER)
LOGGER.addHandler(LOG_FILE)
LOGGER.setLevel(LOGGING_LEVEL)

# Отладка
if __name__ == '__main__':
    LOGGER.critical('Критическая ошибка')
    LOGGER.error('Ошибка')
    LOGGER.debug('Отладочная информация')
    LOGGER.info('Информационное сообщение')