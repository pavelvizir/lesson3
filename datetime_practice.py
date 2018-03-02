#!/usr/bin/env python
'''
Задание:

    1. Напечатайте в консоль даты: вчера, сегодня, месяц назад.
    2. Превратите строку "01/01/17 12:10:03.234567" в объект datetime.

'''

from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta


def get_dates():
    '''1. Напечатайте в консоль даты: вчера, сегодня, месяц назад.'''

    # Отличная возможность поиграть с .format, multiple return etc
    dates = {}
    dates["Сегодня"] = date.today()
    dates["Вчера"] = dates["Сегодня"] + timedelta(days=-1)
    dates["Месяц назад"] = dates["Сегодня"] + relativedelta(months=-1)

    return '\n'.join([
        "{:20}{:>20}".format(k + ":", str(v)) for k, v in dates.items()
    ]), dates


def convert_string_to_date(string=None):
    '''2. Превратите строку "01/01/17 12:10:03.234567" в объект datetime.'''

    # Passing default argument value test
    if string is None:
        string = "01/01/17 12:10:03.234567"

    return datetime.strptime(string, '%m/%d/%y %H:%M:%S.%f')


print("{}\n".format(get_dates()[0]))
# print("\n{}\n".format(get_dates()[1]["Вчера"]))
for arg in [None, "02/03/19 19:30:03.234567"]:
    i = convert_string_to_date(arg)
    print("\t{}\n\t{}\n".format(i, type(i)))
