#!/usr/bin/env python
'''
Задание

    1. Скачайте файл по ссылке.
    2. Прочитайте его и подсчитайте количество слов в тексте.


    TODO: regexp with more delimeters, line by line.

'''


def count_words_in_file(file_name):
    ''' Считает количество слов в файле. '''

    with open(file_name, 'r', encoding='utf-8') as file:
        text = file.read()

        return 'File {} has {} words.'.format(file_name, len(text.split()))


print(count_words_in_file('referat.txt'))
