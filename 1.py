#!/usr/bin/env python
''' TODO: centroid
            permutations
            coord grid
            '''
from csv import reader
from datetime import datetime
from json import loads
from math import hypot  # Выглядит лучше sqrt((x2-x1)**2...

from geopy.distance import VincentyDistance

file_name_bus = 'data-398-2018-02-13.csv'
file_name_metro = 'data-397-2018-02-27.json'
delim = ';'
enc = 'windows-1251'


def get_bus_stops(file_name, encoding, delim):
    global w2
    w2 = datetime.now()
    with open(file_name, 'r', encoding=encoding) as file:
        content = reader(file, delimiter=delim)
        next(content)
        result = set((float(line[3]), float(line[2])) for line in content)

        return result


def get_metro_exits(file_name, encoding):
    global w1
    w1 = datetime.now()
    with open(file_name, 'r', encoding=enc) as file:
        content = loads(file.read())
        result = {}

        for line in content:
            lon, lat = line['geoData']['coordinates']
            station = line['NameOfStation']
            try:
                result[station].append((lat, lon))
            except KeyError:
                result[station] = [
                    (lat, lon),
                ]


        return result


def get_max_bus_stops(metro_coord, bus_coord):
    global w3
    w3 = datetime.now()
    max_station_list = [0, []]
    for station, coord_list in metro_coord.items():
        counter = 0
        a = []
        for exit in coord_list:
            for bus_stop_coord in bus_coord:
                    if bus_stop_coord not in a and VincentyDistance(bus_stop_coord, exit).m <= 2500:
                        a.append(bus_stop_coord)
                        counter += 1
        a.clear()
        if counter > max_station_list[0]:
            max_station_list.clear()
            max_station_list.extend([counter, [
                station,
            ]])
        elif counter == max_station_list[0]:
            max_station_list[1].append(station)
    return max_station_list


print(    get_max_bus_stops(        get_metro_exits(file_name_metro, enc),        get_bus_stops(file_name_bus, enc, delim)))
#get_metro_exits(file_name_metro, enc)

w4 = datetime.now()
print(w2 - w1, w3 - w2, w4 - w3)
