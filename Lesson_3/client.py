import sys
import json
import time
import logging
from socket import *

import logs.logs_configs.client_log_config
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.utils import send_message, get_message



CLIENT_LOGGER = logging.getLogger('client')


# Срипт клиента
def create_presense(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


def process_answer(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'{message[RESPONSE]} : {message[ERROR]}'
    raise ValueError


def main():
    # Получаем IP и port сервера
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}.'
            f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    # Инициализация сокета и обмен
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_address, server_port))

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')
    
    msg_to_server = create_presense()
    send_message(client_socket, msg_to_server)

    try:
        answer = process_answer(get_message(client_socket))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    except (ValueError, json.JSONDecodeError):
        CLIENT_LOGGER.error('Не удалось декодировать сообщение от сервера.')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()


"""
Output:

200 : OK
"""