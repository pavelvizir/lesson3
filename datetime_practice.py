#!/usr/bin/env python
'''
Задание:

    1. Напечатайте в консоль даты: вчера, сегодня, месяц назад.
    2. Превратите строку "01/01/17 12:10:03.234567" в объект datetime.

'''

from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta


def print_dates():
    '''1. Напечатайте в консоль даты: вчера, сегодня, месяц назад.'''
    date_today = date.today()
    date_yesterday = date_today + timedelta(days=-1)
    date_month_ago = date_today + relativedelta(months=-1)
    print()
    print("{:20s}{:>20}".format("Сегодня: ", str(date_today)))
    print("{:20s}{:>20}".format("Вчера: ", str(date_yesterday)))
    print("{:20s}{:>20}".format("Месяц назад: ", str(date_month_ago)))


def convert_string_to_date(string):
    '''2. Превратите строку "01/01/17 12:10:03.234567" в объект datetime.'''

    return datetime.strptime(string, '%m/%d/%y %H:%M:%S.%f')


print_dates()

datetime_string = "01/01/17 12:10:03.234567"
datetime_from_string = convert_string_to_date(datetime_string)
print("\n\t{}\n\t{}".format(type(datetime_from_string), str(datetime_string)))
