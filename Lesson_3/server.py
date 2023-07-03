import json
import sys
import logging
from socket import *

import logs.logs_configs.server_log_config
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.utils import get_message, send_message
from decos import log



SERVER_LOGGER = logging.getLogger('server')

# Скрипт сервера
@log
def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь - ответ для клиента

    :param message:
    :return dict:
    '''
    SERVER_LOGGER.debug(f'Разбор сообщения: {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    # Получаем адрес и порт
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    
    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = DEFAULT_IP_ADDRESS
    except IndexError:
        SERVER_LOGGER.critical(
            'После параметра -\'a\' необходимо указать IP-адрес, который будет слушать сервер.'
        )
        sys.exit(1)


    # Создаем сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((listen_address, listen_port))

    # Слушаем порт
    server_socket.listen(MAX_CONNECTIONS)
    SERVER_LOGGER.info(f'Server is running at {listen_address}:{listen_port}')
    while True:
        client, client_address = server_socket.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.info(f'Сообщение {message_from_client}, от клиента {client_address}')
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.info(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except (ValueError, json.JSONDecodeError):
            SERVER_LOGGER.error(f'Принято некорректное сообщение от {client_address}')
            client.close()


if __name__ == '__main__':
    main()


