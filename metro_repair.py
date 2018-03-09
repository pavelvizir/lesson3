#!/usr/bin/env python
'''
Метро

В этом задании требуется определить, на каких станциях московского метро сейчас
идёт ремонт эскалаторов и вывести на экран их названия.

Файл с данными можно скачать на странице
http://data.mos.ru/opendata/624/row/1773539.

'''

import json
from datetime import datetime


def get_metro_repair():
    ''' Возвращает станции, где сейчас ремонт эскалаторов. '''
    file_name = 'data-397-2018-02-27.json'
    enc = 'windows-1251'
    today = datetime.today()
    with open(file_name, 'r', encoding=enc) as file:
        reader = json.loads(file.read())
        result = set()
        for line in reader:
            for escalator in line['RepairOfEscalators']:
                if escalator:
                    date_range = escalator['RepairOfEscalators'].split('-')
                    if datetime.strptime(date_range[0], '%d.%m.%Y')\
                            <= today <=\
                            datetime.strptime(date_range[1], '%d.%m.%Y'):
                        result.add(line['NameOfStation'])
        return sorted(result)


print(get_metro_repair())
