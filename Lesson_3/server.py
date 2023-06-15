import json
import sys
from socket import *

from common.variables import DEFAULT_IP_ADDRESS, DEFAULT_PORT, MAX_CONNECTIONS, \
    ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR
from common.utils import get_message, send_message



# Скрипт сервера
def process_client_message(message):
    '''
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клиента, проверяет корректность,
    возвращает словарь - ответ для клиента

    :param message:
    :return dict:
    '''

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
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print('В качестве порт может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)
    
    try:
        if '-a' in sys.argv:
            listen_address = int(sys.argv[sys.argv.index('-a') + 1])
        else:
            listen_address = DEFAULT_IP_ADDRESS
    except IndexError:
        print(
            'После параметра -\'a\' необходимо указать IP-адрес, который будет слушать сервер.'
        )
        sys.exit(1)


    # Создаем сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((listen_address, listen_port))

    # Слушаем порт
    server_socket.listen(MAX_CONNECTIONS)
    print(f'Server is running at {listen_address}:{listen_port}')
    while True:
        client, client_address = server_socket.accept()
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_message(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            print(f'Принято некорректное сообщение от {client_address}')
            client.close()


if __name__ == '__main__':
    main()



"""
Output:

Server is running at 127.0.0.1:7777
{'action': 'presence', 'time': 1686864745.4811676, 'user': {'account_name': 'Guest'}}
"""