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
        result = set((float(line[2]), float(line[3])) for line in content)

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
                result[station].append((lon, lat))
            except KeyError:
                result[station] = [
                    (lon, lat),
                ]


        return result


def get_max_bus_stops(metro_coord, bus_coord):
    global w3
    w3 = datetime.now()
    max_station_list = [
        0,
    ]
    i = 1
    for station, coord_list in metro_coord.items():
#        if i > 19:
#            break

        counter = 0
        a = []
 #       a = set()
   #     m_lon, m_lat = coord_list[0]
 #       c = set((lon, lat) for lon, lat in bus_coord
  #              if hypot(m_lon - lon, m_lat - lat) < 0.012)

        for exit in coord_list:
#            e_lon, e_lat = exit

            for bus_stop_coord in bus_coord:
#                if hypot(e_lon - bus_stop_coord[0],
#                         e_lat - bus_stop_coord[1]) < 0.0057:

                    if bus_stop_coord not in a and VincentyDistance(bus_stop_coord, exit).m <= 250:
                        a.append(bus_stop_coord)
                        # a.add(bus_stop_coord)
                        counter += 1

#            for b in a:
 #               c.remove(b)
 #               bus_coord.remove(b)

        a.clear()

        if counter > max_station_list[0]:
            max_station_list.clear()
            max_station_list.extend([counter, [
                station,
            ]])
        elif counter == max_station_list[0]:
            max_station_list[1].append(station)
        i+=1

    return max_station_list


print(    get_max_bus_stops(        get_metro_exits(file_name_metro, enc),        get_bus_stops(file_name_bus, enc, delim)))
#get_metro_exits(file_name_metro, enc)

w4 = datetime.now()
print(w2 - w1, w3 - w2, w4 - w3)
