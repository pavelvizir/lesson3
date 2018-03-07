#!/usr/bin/env python
'''
Остановки у метро

    Объединить наборы данных из предыдущих задач и посчитать,
    у какой станции метро больше всего остановок (в радиусе 0.5 км).
'''

from csv import reader
from json import loads

from geopy.distance import distance
# from geopy.distance import VincentyDistance
#from math import hypot
#from itertools import permutations
from datetime import datetime

file_name_bus = 'data-398-2018-02-13.csv'
file_name_metro = 'data-397-2018-02-27.json'
delim = ';'
enc = 'windows-1251'
radius = 500


def get_bus_stops(file_name, encoding, delimiter):
    ''' Получаем набор (широта, долгота) остановок (3 и 2 столбцы). '''
    with open(file_name, 'r', encoding=encoding) as file:
        content = reader(file, delimiter=delimiter)
        next(content)  # Пропускаем заголовки
        result = sorted(
            set((float(line[3]), float(line[2])) for line in content))

        return result


def get_metro_exits(file_name, encoding):
    ''' Получаем словарь из станций и списка (широта, долгота) выходов. '''
    with open(file_name, 'r', encoding=encoding) as file:
        content = loads(file.read())
        result = {}

        for line in content:
            lon, lat = line['geoData']['coordinates']
            station = line['NameOfStation']
            try:
                result[station].append((lat, lon))
            except KeyError:
                result[station] = [(lat, lon), ]

        return result


def get_max_bus_stops(metro, bus):
    ''' Возвращает максимальное количество остановок
        и список станций в отформатированном виде. '''
    max_lat = max([lat for lat, lon in bus])
    # Длина градуса долготы на верхней границе широт в словаре автобусов.
    lon_m = radius / distance((max_lat, 0), (max_lat, 1)).m
    lat_m = radius / 110500  # Нижняя граница длины градуса широты 110.574 км.
    result = [0, []]
    counted_for_station = set()

    for station, coord_list in metro.items():
        counter = 0
        busa =    set()
        a = [a for a,b in coord_list]
 #       b = [b for a,b in coord_list]
 #       print(min(a), max(a), min(b), max(b))
        mina = min(a)
        maxa = max(a)
        for a1, b1 in bus:
            if a1 >=    mina - lat_m:
                if a1 <= maxa + lat_m:
                    busa.add((a1, b1))
                else:
                    break
                    
        for station_exit in coord_list:
            slat = station_exit[0]
            slon = station_exit[1]

            for bus_stop_coord in busa:
               # lat_diff = bus_stop_coord[0] - slat
            #    if lat_diff > lat_m:
                #    break
                if (
                     #   abs(lat_diff) < lat_m and
                        abs(bus_stop_coord[1] - slon) < lon_m and
                        bus_stop_coord not in counted_for_station and
                        distance(bus_stop_coord, station_exit).m <= radius
                ):
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
#print(bus_stops)
