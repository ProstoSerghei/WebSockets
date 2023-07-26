import argparse
import logging
import select
import socket
import sys
import time
import threading

from common.utils import get_message, send_message
import logs.logs_configs.server_log_config
from decos import log
from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, \
    MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_200, RESPONSE_400, \
    DESTINATION, EXIT
from metaclasses import ServerMaker
from descriptors import Port
from db import ServerStorage


SERVER_LOGGER = logging.getLogger('server')


class Server(threading.Thread, metaclass=ServerMaker):
    port = Port()

    def __init__(self, listen_addr, listen_port, db):
        self.addr = listen_addr
        self.port = listen_port
        
        self.db = db

        self.clients = []
        self.messages = []
        self.names = dict()

        super().__init__()

    def init_socket(self):
        SERVER_LOGGER.info(f'Запущен сервер: {self.addr}:{self.port}')

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.bind((self.addr, self.port))
        server_sock.settimeout(0.5)
        
        self.sock = server_sock
        self.sock.listen()

    def run(self):
        self.init_socket()

        while True:
            try:
                client, client_addres = self.sock.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соединение с {client_addres}')
                self.clients.append(client)
            
            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(
                        self.clients, 
                        self.clients, 
                        [], 
                        0
                    )
            except OSError: 
                pass

            if recv_data_lst:
                for client_with_mess in recv_data_lst:
                    try:
                        self.process_client_message(
                            get_message(client_with_mess),
                            client_with_mess
                        )
                    except:
                        SERVER_LOGGER.info(f'{client_with_mess.getpeername()} отключился от сервера.')
                        self.clients.remove(client_with_mess)
            
            for message in self.messages:
                try:
                    self.process_message(message, send_data_lst)
                except Exception as e:
                    SERVER_LOGGER.info(f'Соединение с {message[DESTINATION]} потеряно\n{e}')
                    self.clients.remove(self.names[message[DESTINATION]])
                    del self.names[message[DESTINATION]]
                self.messages.clear()

    def process_client_message(self, message, client):
        SERVER_LOGGER.info(f'Разбор сообщения от клиента : {message}')

        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message:
            if message[USER][ACCOUNT_NAME] not in self.names.keys():
                self.names[message[USER][ACCOUNT_NAME]] = client
                client_ip, client_port = client.getpeername()
                self.db.user_login(message[USER][ACCOUNT_NAME], client_ip, client_port)
                send_message(client, RESPONSE_200)
            else:
                response = RESPONSE_400
                response[ERROR] = 'Имя уже занято'
                send_message(client, response)
                self.clients.remove(client)
                client.close()
            return
        elif ACTION in message and message[ACTION] == MESSAGE and DESTINATION in message \
            and TIME in message and SENDER in message and MESSAGE_TEXT in message:
            self.messages.append(message)
            return
        elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
            self.db.user_logout(message[ACCOUNT_NAME])
            self.clients.remove(self.names[ACCOUNT_NAME])
            del self.names[ACCOUNT_NAME]
            return
        else:
            response = RESPONSE_400
            response[ERROR] = 'Запрос некорректный.'
            send_message(client, response)
            return
        


    def process_message(self, message, listen_socks):
        if message[DESTINATION] in self.names and self.names[message[DESTINATION]] in listen_socks:
            send_message(self.names[message[DESTINATION]], message)
            SERVER_LOGGER.info(
                f'Отправлено сообщение пользователю {message[DESTINATION]}'
                f' от пользователя {message[SENDER]}.')
        elif message[DESTINATION] in self.names and self.names[message[DESTINATION]] not in listen_socks:
            raise Exception
        else:
            SERVER_LOGGER.error(f'Пользователь {message[DESTINATION]} не зарегистрирован.')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_port = namespace.p
    listen_address = namespace.a

    return listen_address, listen_port


def print_help():
    print('Поддерживаемые комманды:')
    print('users - список известных пользователей')
    print('connected - список подключенных пользователей')
    print('loghist - история входов пользователя')
    print('exit - завершение работы сервера.')
    print('help - вывод справки по поддерживаемым командам')


def main():
    listen_addr, listen_port = arg_parser()

    db = ServerStorage()

    server = Server(listen_addr, listen_port, db)
    server.daemon = True
    server.start()

    while True:
        command = input('Введите комманду: ')
        if command == 'help':
            print_help()
        elif command == 'exit':
            break
        elif command == 'users':
            for user in sorted(db.users_list()):
                print(f'Пользователь {user[0]}, последний вход: {user[1]}')
        elif command == 'connected':
            for user in sorted(db.active_users_list()):
                print(f'Пользователь {user[0]}, подключен: {user[1]}:{user[2]}, время установки соединения: {user[3]}')
        elif command == 'loghist':
            name = input('Введите имя пользователя для просмотра истории. Для вывода всей истории, просто нажмите Enter: ')
            for user in sorted(db.login_history(name)):
                print(f'Пользователь: {user[0]} время входа: {user[1]}. Вход с: {user[2]}:{user[3]}')
        else:
            print('Команда не распознана.')

if __name__ == '__main__':
    main()