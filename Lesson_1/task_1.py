'''
1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode и также проверить тип и содержимое переменных.
'''



def unicode_converter(input_str):
    res = input_str.encode('unicode-escape')
            
    return res.decode('utf-8')


russian_words_arr = ['разработка', 'сокет', 'декоратор']
russian_words_unicode_arr = [
    '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430', 
    '\u0441\u043e\u043a\u0435\u0442', 
    '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'
    ]

for i in range(0, len(russian_words_arr)):
    print('str:' , russian_words_arr[i])
    print('Unicode str:' , russian_words_unicode_arr[i])
    print('Uncode points:', unicode_converter(russian_words_arr[i]))
    print('Type of str:', type(russian_words_arr[i]))
    print('Type of unicode str:', type(russian_words_unicode_arr[i]))
    print('\n')





'''
Output:

str: разработка
Unicode str: разработка
Uncode points: \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430
Type of str: <class 'str'>
Type of unicode str: <class 'str'>


str: сокет
Unicode str: сокет
Uncode points: \u0441\u043e\u043a\u0435\u0442
Type of str: <class 'str'>
Type of unicode str: <class 'str'>


str: декоратор
Unicode str: декоратор
Uncode points: \u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440
Type of str: <class 'str'>
Type of unicode str: <class 'str'>
'''