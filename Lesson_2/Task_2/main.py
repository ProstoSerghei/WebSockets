'''
2. Задание на закрепление знаний по модулю json. 
Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными. 
Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — 
товар (item), 
количество (quantity), 
цена (price), 
покупатель (buyer), 
дата (date). 
Функция должна предусматривать запись данных в виде словаря в файл orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
'''
import json




DATA = [
    {
        'item': 'Принтер',
        'quantity': 1,
        'price': 49.99,
        'buyer': 'Alex S.',
        'date': '10.06.2023',
    },
    {
        'item': 'Scaner',
        'quantity': 2,
        'price': 29.99,
        'buyer': 'Jason D.',
        'date': '07.06.2023',
    },
    {
        'item': 'Monitor',
        'quantity': 4,
        'price': 89.99,
        'buyer': 'Abram G.',
        'date': '10.06.2023',
    },
]

FILE_NAME = './orders.json'



def write_order_to_json(item, quantity, price, buyer, date, file_name=''):
    init_data = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date,
    }
    res_data = {}

    with open(file_name, 'r', encoding='utf-8') as f:
        res_data = json.load(f)
        res_data['orders'].append(init_data)

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(res_data, f, indent=4, ensure_ascii= False)




for data in DATA:
    write_order_to_json(*data.values(), file_name=FILE_NAME)