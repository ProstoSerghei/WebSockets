import sys
import json
import time
from socket import *

from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.utils import send_message, get_message




# Срипт клиента
def create_presense(account_name='Guest'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out


def process_answer(message):
    '''
    Функция разбирает ответ сервера
    :param message:
    :return:
    '''
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
        print('В качестве порт может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Инициализация сокета и обмен
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    msg_to_server = create_presense()
    send_message(client_socket, msg_to_server)

    try:
        answer = process_answer(get_message(client_socket))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение от сервера.')


if __name__ == '__main__':
    main()


"""
Output:

200 : OK
"""