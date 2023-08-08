"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
from pprint import pprint
from ipaddress import ip_address
from subprocess import Popen, PIPE




def host_range_ping(ip: str, ip_range: int):
    ipv4 = ip_address(ip)
    res = {}
    for i in range(ip_range + 1):
        current_ip = ipv4 + i
        command = f'ping {current_ip} -n 1'
        reply = Popen(command, stdout=PIPE, stderr=PIPE)
        code = reply.wait()
        if code == 0:
            res[current_ip] = 'Узел доступен'
        else:
            res[current_ip] = 'Узел недоступен'
    pprint(res)
    return res



if __name__ == '__main__':
    ip = '192.168.1.0'
    host_range_ping(ip, 20)


"""
Output:

{IPv4Address('192.168.1.0'): 'Узел доступен',
 IPv4Address('192.168.1.1'): 'Узел доступен',
 IPv4Address('192.168.1.2'): 'Узел недоступен',
 IPv4Address('192.168.1.3'): 'Узел доступен',
 IPv4Address('192.168.1.4'): 'Узел доступен',
 IPv4Address('192.168.1.5'): 'Узел доступен',
 IPv4Address('192.168.1.6'): 'Узел доступен',
 IPv4Address('192.168.1.7'): 'Узел доступен',
 IPv4Address('192.168.1.8'): 'Узел доступен',
 IPv4Address('192.168.1.9'): 'Узел доступен',
 IPv4Address('192.168.1.10'): 'Узел доступен',
 IPv4Address('192.168.1.11'): 'Узел доступен',
 IPv4Address('192.168.1.12'): 'Узел доступен',
 IPv4Address('192.168.1.13'): 'Узел доступен',
 IPv4Address('192.168.1.14'): 'Узел доступен',
 IPv4Address('192.168.1.15'): 'Узел доступен',
 IPv4Address('192.168.1.16'): 'Узел доступен',
 IPv4Address('192.168.1.17'): 'Узел доступен',
 IPv4Address('192.168.1.18'): 'Узел доступен',
 IPv4Address('192.168.1.19'): 'Узел доступен',
 IPv4Address('192.168.1.20'): 'Узел доступен'}
"""