import sys
import json
import time
import logging
import argparse
import threading
from socket import *

import logs.logs_configs.client_log_config
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, \
    MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT
from common.utils import send_message, get_message
from decos import log


CLIENT_LOGGER = logging.getLogger('client')


# Срипт клиента

@log
def create_exit_message(username):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: username
    }


@log
def create_presense(account_name):
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
def message_from_server(sock, my_username):
    # Обработчик сообщений от других пользователей
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and \
                    SENDER in message and DESTINATION in message\
                    and MESSAGE_TEXT in message and message[DESTINATION] == my_username:
                print(f'\nПолучено сообщение от пользователя {message[SENDER]}:'
                      f'\n{message[MESSAGE_TEXT]}')
                CLIENT_LOGGER.info(f'Сообщение от {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
            else:
                CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')
        except Exception as e:
            CLIENT_LOGGER.error(f'Произошла ошибка:\n{e}')
            break


@log
def create_message(sock, username='Guest'):
    # Запрос текста сообщения
    to_user = input('Введите получателя: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: username,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message
    }
    try:
        send_message(sock, message_dict)
        CLIENT_LOGGER.info(f'Отправлено сообщение: {message_dict}')
    except:
        CLIENT_LOGGER.critical('Потеряно соединение с сервером.')
        sys.exit(1)


@log
def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения.')
            time.sleep(0.5)
            break
        else:
            print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)


    return server_address, server_port, client_name


def print_help():
    """Функция выводящяя справку по использованию"""
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')


def main():
    print('Запуск консольного месседжера. Клиентский модуль.')
    # Получаем IP и port сервера
    server_address, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Введите имя пользоватля: ')
    
    print(f'Выполнен вход под имененм {client_name}.')

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: имя - {client_name}'
                       f'адрес сервера: {server_address}, порт: {server_port}')
    # Инициализация сокета и обмен
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_address, server_port))
        send_message(client_socket, create_presense(client_name))
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
        receiver = threading.Thread(target=message_from_server, args=(client_socket, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(client_socket, client_name))
        user_interface.daemon = True
        user_interface.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break




if __name__ == '__main__':
    main()


"""
Output:

200 : OK
"""