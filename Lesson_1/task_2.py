'''
2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.
'''


bytes_words = [b'class', b'function', b'method']


for i in bytes_words:
    print('Type:', type(i))
    print('Сontent:', i)
    print('Length:', len(i))
    print('\n')


'''
Output:

Type: <class 'bytes'>
Сontent: b'class'
Length: 5


Type: <class 'bytes'>
Сontent: b'function'
Length: 8


Type: <class 'bytes'>
Сontent: b'method'
Length: 6

'''