#!/usr/bin/env python
'''
Остановки у метро

    Объединить наборы данных из предыдущих задач и посчитать,
    у какой станции метро больше всего остановок (в радиусе 0.5 км).
'''

from csv import reader
from json import loads

from geopy.distance import VincentyDistance
#from math import abs
from datetime import datetime

file_name_bus = 'data-398-2018-02-13.csv'
file_name_metro = 'data-397-2018-02-27.json'
delim = ';'
enc = 'windows-1251'


def get_bus_stops(file_name, encoding, delimiter):
    ''' Получаем набор координат остановок (2 и 3 столбцы). '''
    with open(file_name, 'r', encoding=encoding) as file:
        content = reader(file, delimiter=delimiter)
        next(content)  # Пропускаем заголовки
        result = set((float(line[2]), float(line[3])) for line in content)

        return result


def get_metro_exits(file_name, encoding):
    ''' Получаем словарь из станций и списка координат выходов. '''
    with open(file_name, 'r', encoding=encoding) as file:
        content = loads(file.read())
        result = {}

        for line in content:
            lon, lat = line['geoData']['coordinates']
            station = line['NameOfStation']
            try:
                result[station].append((lon, lat))
            except KeyError:
                result[station] = [(lon, lat), ]

        return result


def get_max_bus_stops(metro_coord, bus_coord):
    ''' Возвращает максимальное количество остановок
        и список станций в отформатированном виде. '''
    lat_m = 500/111000
    lon_m = 500/63000
    result = list([0, ])
    counted_for_station = set()

    for station, coord_list in metro_coord.items():
        counter = 0
        #print(station)

        for station_exit in coord_list:
            slat =    station_exit[1]
            slon =    station_exit[0]
            for bus_stop_coord in bus_coord:
                if abs(bus_stop_coord[0] - slon) < lon_m:
                    #if  abs(bus_stop_coord[1] - slat) < lat_m:
                        if bus_stop_coord not in counted_for_station:
                            if VincentyDistance(bus_stop_coord, station_exit).m <= 500:
                                counted_for_station.add(bus_stop_coord)
                                counter += 1
        counted_for_station.clear()

        if counter > result[0]:
            result.clear()
            result.extend([counter, [
                station,
            ]])
        elif counter == result[0]:
            result[1].append(station)

    return result

bus_stops = get_bus_stops(file_name_bus, enc, delim)
metro_exits = get_metro_exits(file_name_metro, enc)
w =    datetime.now()
max_bus_stop = get_max_bus_stops(metro_exits, bus_stops)
print(max_bus_stop, datetime.now() - w)
