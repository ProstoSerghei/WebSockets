'''
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести его содержимое.
'''
import os


DATA = [
    'сетевое программирование',
    'сокет',
    'декоратр'
]

os.system('chardetect test_file.txt')


# with open('test_file.txt', 'w') as f:
#     for line in DATA:
#         f.write(f'{line}\n')


with open('test_file.txt', 'r', encoding='utf-8') as f:
    for line in f:
        print(line, end='')



'''
Output:

test_file.txt: utf-8 with confidence 0.99

сетевое программирование
сокет
декоратр
'''