import sys
import json
import time
import logging
import argparse
from socket import *

import logs.logs_configs.client_log_config
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, \
    MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import send_message, get_message
from decos import log


CLIENT_LOGGER = logging.getLogger('client')


# Срипт клиента
@log
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


@log
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
        elif message[RESPONSE] == 400:
            return f'{message[RESPONSE]} : {message[ERROR]}'
    raise ValueError


@log
def message_from_server(message):
    # Обработчик сообщений от других пользователей
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, username='Guest'):
    # Запрос текста сообщения
    message = input('Введите сообщение для отправки или \'exit\' для выхода: ')
    if message == 'exit':
        sock.close()
        CLIENT_LOGGER.info(f'Пользователь {username} выходит из чата.')
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: username,
        MESSAGE_TEXT: message
    }
    return message_dict
        


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(f'Указан недопустимый режим работы {client_mode}, '
                        f'допустимые режимы: listen , send')
        sys.exit(1)

    return server_address, server_port, client_mode


def main():
    # Получаем IP и port сервера
    server_address, server_port, client_mode = arg_parser()


    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')
    # Инициализация сокета и обмен
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        send_message(client_socket, create_presense())
        response = process_answer(get_message(client_socket))
        CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {response}')
        print(f'Установлено соединение с сервером. Ответ сервера: {response}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except Exception as e:
        CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {e}')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы - отправка сообщений.')
        else: 
            print('Режим работы - приём сообщений.')
        
        while True:
            # Send mode
            if client_mode == 'send':
                try:
                    send_message(client_socket, create_message(client_socket))
                except Exception as e:
                    CLIENT_LOGGER.error(f'При установке соединения сервер вернул ошибку: {e}')
                    sys.exit(1)

            # Listen mode
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(client_socket))
                except Exception as e:
                    CLIENT_LOGGER.error(f'Соединение с сервером {server_address} было потеряно.')
                    sys.exit(1)




if __name__ == '__main__':
    main()


"""
Output:

200 : OK
"""