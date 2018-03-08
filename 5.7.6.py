#!/usr/bin/env python
'''
Остановки у метро

    Объединить наборы данных из предыдущих задач и посчитать,
    у какой станции метро больше всего остановок (в радиусе 0.5 км).

    TODO:
    0 метров
    positive integer
    sort station results
    вынести метр наружу
    0 станций обработать
    copy basic function here as well, for reference
'''

from csv import reader
from datetime import datetime
from json import loads
# from geopy.distance import VincentyDistance
from math import hypot

from geopy.distance import distance

file_name_bus = 'data-398-2018-02-13.csv'
file_name_metro = 'data-397-2018-02-27.json'
delim = ';'
enc = 'windows-1251'
radius = 500
rounding = 0.001

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
                result[station].add((lat, lon))
            except KeyError:
                result[station] = {(lat, lon)}

        return result


def get_max_bus_stops(metro, bus):
    ''' Возвращает максимальное количество остановок
        и список станций в отформатированном виде. '''
    # Как быстро достать первый и последний элементы сета?
    # ? next(iter(bus)) - должен достать первый
    bus_lat_list = [lat for lat, lon in bus]

    if abs(bus_lat_list[0]) > abs(bus_lat_list[-1]):
        max_bus_lat = bus_lat_list[0]
        min_bus_lat = bus_lat_list[-1]
    else:
        max_bus_lat = bus_lat_list[-1]
        min_bus_lat = bus_lat_list[0]
    # Длина градуса долготы на верхней границе широт в словаре автобусов.
    lower_lon_m = (1 / distance((min_bus_lat, 0), (min_bus_lat, 1)).m) * (1 - rounding)
    upper_lon_m = (1 / distance((max_bus_lat, 0), (max_bus_lat, 1)).m) * (1 + rounding)
    # print(upper_lon_m, lower_lon_m)
    upper_lon_rad = radius * upper_lon_m
    # max_lat_rad = radius * lower_lon_m
    # lon_x = (radius - max(1, radius/100)) / upper_lon_m
    #max_lat_m = 1 / 110500
    upper_lat_m = 1 / 110500
    lower_lat_m = 1 / 111700
    # Нижняя граница длины градуса широты 110.574 км.
    upper_lat_rad = radius * upper_lat_m
    # 111699
    result = [0, []]
    counted_for_station = set()
    counter_2 = 0
    for station, station_coord_list in metro.items():
        counter = 0
        bus_reduced = set()
        metro_lat_list = [lat for lat, lon in station_coord_list]
        min_metro_lat = min(metro_lat_list)
        max_metro_lat = max(metro_lat_list)

        for lat, lon in bus:
            if lat >= min_metro_lat - upper_lat_rad:
                if lat <= max_metro_lat + upper_lat_rad:
                    bus_reduced.add((lat, lon))
                else:
                    break
        #print(len(bus_reduced))
        for station_exit in station_coord_list:
            exit_lat, exit_lon = station_exit

            for bus_stop in bus_reduced:
             # for bus_stop in bus:
                bus_lat, bus_lon = bus_stop
                # if bus_stop not in bus_reduced:
                #    if distance(bus_stop, station_exit).m <= radius:
                #        print('FUCK')


                if (abs(bus_lon - exit_lon) < upper_lon_rad
                        and bus_stop not in counted_for_station):
                    if hypot(((bus_lat - exit_lat) / upper_lat_m),
                             ((bus_lon - exit_lon) / upper_lon_m)) > radius:
                        # if distance(bus_stop, station_exit).m <= radius:
                        #    print('fuck')
                        continue
                    elif hypot(((bus_lat - exit_lat) / lower_lat_m), ((bus_lon - exit_lon) / lower_lon_m)) < radius:
                        # if distance(bus_stop, station_exit).m > radius:
                        #    print('fuck')
                        counted_for_station.add(bus_stop)
                        counter += 1
                    elif distance(bus_stop, station_exit).m <= radius:
                        counter_2 +=1
                        counted_for_station.add(bus_stop)
                        counter += 1

                # else:
                #    if bus_stop not in counted_for_station:
                #        if distance(bus_stop, station_exit).m <= radius:
                #            print('FUCK')
        counted_for_station.clear()

        if counter > result[0]:
            result.clear()
            result.extend([counter, [
                station,
            ]])
        elif counter == result[0]:
            result[1].append(station)
#        break
    fresult = 'В радиусе {} {} от выходов из метро больше всего автобусных остановок ({}) на {} метро {}.'.format(
        radius, 'метров' if radius > 1 else 'метра', result[0], 'станциях'
        if len(result[1]) > 1 else 'станции', ', '.join(result[1]))
    print(counter_2)
    return fresult


bus_stops = get_bus_stops(file_name_bus, enc, delim)
metro_exits = get_metro_exits(file_name_metro, enc)
w1 = datetime.now()
max_bus_stop = get_max_bus_stops(metro_exits, bus_stops)
print(max_bus_stop, datetime.now() - w1)
