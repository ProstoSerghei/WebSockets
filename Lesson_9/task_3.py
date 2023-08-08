"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок
"""
from ipaddress import ip_address
from subprocess import Popen, PIPE

from tabulate import tabulate




def host_range_ping(ip: str, ip_range: int):
    ipv4 = ip_address(ip)
    available = []
    not_available = []
    res = {}
    for i in range(ip_range + 1):
        current_ip = ipv4 + i
        command = f'ping {current_ip} -n 1'
        reply = Popen(command, stdout=PIPE, stderr=PIPE)
        code = reply.wait()
        if code == 0:
            available.append(current_ip)
        else:
            not_available.append(current_ip)
    res['Доступные узлы'] = available
    res['Недоступные узлы'] = not_available
    return res



if __name__ == '__main__':
    ip = '192.168.1.0'
    res = host_range_ping(ip, 5)
    print(tabulate(res, headers='keys', tablefmt="grid"))


"""
Output:

+------------------+--------------------+
| Доступные узлы   | Недоступные узлы   |
+==================+====================+
| 192.168.1.0      | 192.168.1.2        |
+------------------+--------------------+
| 192.168.1.1      | 192.168.1.5        |
+------------------+--------------------+
| 192.168.1.3      |                    |
+------------------+--------------------+
| 192.168.1.4      |                    |
+------------------+--------------------+
"""