#!/usr/bin/env python
'''
Остановки

Считать из csv-файла (с http://data.mos.ru/datasets/752) количество остановок,
вывести улицу, на которой больше всего остановок.

'''

import csv
from collections import Counter


def get_popular_street():
    ''' Получаем улицу с самым большим кол-вом остановок. '''
    file_name = 'data-398-2018-02-13.csv'
    delim = ';'
    enc = 'windows-1251'
    with open(file_name, 'r', encoding=enc) as file:
        reader = csv.reader(file, delimiter=delim)
        streets = [row[4] for row in reader]
    # С Counter действительно удобнее оказалось.
    return Counter(streets).most_common(1)


print(get_popular_street())
