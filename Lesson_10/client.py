import argparse
import json
import logging
from socket import AF_INET, SOCK_STREAM, socket
import sys
import threading
import time

import logs.logs_configs.client_log_config
from metaclasses import ClientMaker
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, \
    MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT
from common.utils import send_message, get_message
from decos import log



CLIENT_LOGGER = logging.getLogger('client')

class ClientSender(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def create_exit_message(self):
        return {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.account_name
        }
    
    def create_message(self):
        to = input('Введите имя получателя: ')
        message = input('Введите сообщение: ')
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.account_name,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:
            send_message(self.sock, message_dict)
            CLIENT_LOGGER.info(f'Отправлено сообщение {to}')
        except:
            CLIENT_LOGGER.info(f'Потеряно соединение с сервером.')
            exit(1)

    def run(self):
        self.print_help()
        while True:
            command = input('Введите команду: ').lower()
            if command == 'message':
                self.create_message()
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                try:
                    send_message(self.sock, self.create_exit_message())
                except:
                    pass
                print('Вы были отключены от сервера.')
                CLIENT_LOGGER.info(f'Завершение работы по команде пользователя.')
                time.sleep(0.5)
                break
            else:
                print('Неизвестная команда. Попробуйте еще раз')
    
    def print_help(self):
        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')


class ClientReader(threading.Thread, metaclass=ClientMaker):
    def __init__(self, account_name, sock):
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    def run(self):
        while True:
            try:
                message = get_message(self.sock)
                if ACTION in message and message[ACTION] == MESSAGE and SENDER in message \
                    and DESTINATION in message and message[DESTINATION] == self.account_name:
                    print(f'\nНовое сообщение от {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                    CLIENT_LOGGER.info(f'\nНовое сообщение от {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
                else:
                    CLIENT_LOGGER.error(f'Некорректное сообщение от сервера:\n{message}')
            except Exception as e:
                CLIENT_LOGGER.error(f'Неизвестная ошибка:\nСообщение: {message}\nОшибка:{e}')
            


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
        receiver = ClientReader(client_name, client_socket)
        receiver.daemon = True
        receiver.start()

        user_interface = ClientSender(client_name, client_socket)
        user_interface.daemon = True
        user_interface.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break




if __name__ == '__main__':
    main()