#!/usr/bin/env python
'''
    Задание

    1. Возьмите словарь с ответами из функции get_answer
    2. Запишите его содержимое в формате csv в формате: "ключ"; "значение".
        Каждая пара ключ-значение должна располагаться на отдельной строке.
'''

import csv


def write_to_csv(file_name, fields, delim, dictionary):
    ''' Записывает словарь в csv-файл. '''

    with open(file_name, 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fields, delimiter=delim)
        writer.writeheader()
        writer.writerows([{
            fields[0]: a,
            fields[1]: b
        } for a, b in dictionary.items()])


def read_from_csv(file_name, fields, delim):
    ''' Читает из csv-файла построчно. '''

    with open(file_name, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, fields, delimiter=delim)

        for line in reader:
            print(line)


def write_and_read_csv(file, fields, delim):
    ''' Последовательно пишет словарь в csv-файл и читает из файла. '''

    answers = {
        "привет": "И тебе привет!",
        "как дела": "Лучше всех!",
        "пока": "Увидимся."
    }
    write_to_csv(file, fields, delim, answers)
    read_from_csv(file, fields, delim)


write_and_read_csv('csv_result.csv', ['ключ', 'значение'], ';')
