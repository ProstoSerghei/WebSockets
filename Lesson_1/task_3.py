'''
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
'''


words = ['attribute', 'класс', 'функция', 'type']

result = []
for word in words:
    try:
        bytes(word, 'ASCII')
    except UnicodeEncodeError:
        result.append(word)

print('Words that cannot be written in byte type:', result)


'''
Output:

>>> Words that cannot be written in byte type: ['класс', 'функция']
'''