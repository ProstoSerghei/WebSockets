import subprocess
from os import path




PROCESS = []
path_to_python = path.abspath('../venv/Scripts/python.exe')
path_to_server = path.abspath('./server.py')
while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, x - закрыть все окна: ')
    
    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESS.append(subprocess.Popen([path_to_python, path_to_server],
                                        creationflags=subprocess.CREATE_NEW_CONSOLE)
                                        )
        PROCESS.append(subprocess.Popen('python client.py -n serghei',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n vlad',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
        PROCESS.append(subprocess.Popen('python client.py -n petro',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()