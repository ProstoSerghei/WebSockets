'''
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в байтовое и выполнить обратное преобразование (используя методы encode и decode).
'''

words = ['разработка', 'администрирование', 'protocol', 'standard']

for word in words:
    word_b = word.encode('utf-8')
    print('Encdoe to bytes:', word_b)
    print('Decode to str (UTF-8):', word_b.decode('utf-8'))
    print('\n')


'''
Output:

Encdoe to bytes: b'\xd1\x80\xd0\xb0\xd0\xb7\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xba\xd0\xb0'
Decode to str (UTF-8): разработка


Encdoe to bytes: b'\xd0\xb0\xd0\xb4\xd0\xbc\xd0\xb8\xd0\xbd\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5'
Decode to str (UTF-8): администрирование


Encdoe to bytes: b'protocol'
Decode to str (UTF-8): protocol


Encdoe to bytes: b'standard'
Decode to str (UTF-8): standard

'''