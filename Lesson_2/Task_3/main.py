'''
3. Задание на закрепление знаний по модулю yaml. 
Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. 

Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, 
второму — целое число, 
третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в кодировке ASCII (например, €);

Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. 
При этом обеспечить стилизацию файла с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
'''
import yaml




DATA ={
    'items': [
        'computer',
        'mouse',
        'keyboard',
        'printer',
    ],
    'items_price': {
        'computer': '200\u20AC-1000\u20AC',
        'keyboard': '5\u20AC-50\u20AC',
        'mouse': '4\u20AC-7\u20AC',
        'printer': '100\u20AC-300\u20AC',
    },
    'items_quantity': 5
}

FILE_NAME = 'res.yaml'

with open(FILE_NAME, 'w', encoding='utf-8') as f:
    yaml.dump(DATA, f, allow_unicode=True, default_flow_style=False)


with open(FILE_NAME, 'r', encoding='utf-8') as f:
    file_data = yaml.load(f, Loader=yaml.FullLoader)
    print((file_data == DATA))
    # >>> True