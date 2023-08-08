"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
from pprint import pprint
from subprocess import Popen, PIPE



HOSTS_LIST = [
    'ya.ru', 
    '192.168.0.111',
    'gb.ru', 
    'github.com', 
    'www.youtube.com', 
    'www.google.ru'
    ]


def host_ping(hosts):
    res = {}
    for host in hosts:
        command = f'ping {host} -n 3'
        reply = Popen(command, stdout=PIPE, stderr=PIPE)
        code = reply.wait()
        if code == 0:
            res[host] = 'Узел доступен'
        else:
            res[host] = 'Узел недоступен'
    pprint(res)
    return res



if __name__ == '__main__':
    host_ping(HOSTS_LIST)


"""
Output:

{'192.168.0.111': 'Узел недоступен',
 'gb.ru': 'Узел доступен',
 'github.com': 'Узел доступен',
 'www.google.ru': 'Узел доступен',
 'www.youtube.com': 'Узел доступен',
 'ya.ru': 'Узел доступен'}
"""