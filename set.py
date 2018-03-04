#!/usr/bin/env python
from json import loads
from csv import reader
from geopy.distance import VincentyDistance
from math import sqrt

file_name_bus = 'data-398-2018-02-13.csv'
file_name_metro='data-397-2018-02-27.json'
delim = ';'
enc = 'windows-1251'
def get_bus_stops(file_name, encoding):
    with open(file_name, 'r', encoding=encoding) as file:
        reader1 = reader(file, delimiter=delim)
        bus_coord = set()
        next(reader1)
    
        for line in reader1:
                bus_coord.add((float(line[2]), float(line[3])))
                
        return bus_coord


def get_metro_exits(file_name, encoding):
    with open(file_name, 'r', encoding=enc) as file:
        reader2 = loads(file.read())
        metro_coord = {}
        i = 1
    
        for line in reader2:
                try:
                    metro_coord[line['NameOfStation']].append((line['geoData']['coordinates'][0], line['geoData']['coordinates'][1]))
                except KeyError:
                    metro_coord[line['NameOfStation']] = [(line['geoData']['coordinates'][0], line['geoData']['coordinates'][1]),]

        return metro_coord

def get_max_bus_stops(metro_coord, bus_coord):
    max_station_list = [0,]
    
    for station, coord_list in metro_coord.items():
        counter = 0
        a = []
        c = set()
    
        for bus_stop_coord in bus_coord:
            if sqrt((coord_list[0][0] - bus_stop_coord[0])**2 + (coord_list[0][1] - bus_stop_coord[1])**2) < 0.012:
                c.add(bus_stop_coord)
    
        for exit in coord_list:
    
            for bus_stop_coord in c:
                if sqrt((exit[0] - bus_stop_coord[0])**2 + (exit[1] - bus_stop_coord[1])**2) < 0.0057:
                    if VincentyDistance(bus_stop_coord, exit).m <= 500:
                        a.append(bus_stop_coord)
                        counter+=1
    
            for b in a:
                c.remove(b)
                bus_coord.remove(b)
    
            a.clear()
    
        if counter > max_station_list[0]:
            max_station_list.clear()
            max_station_list.extend([counter, [station,]])
        elif counter == max_station_list[0]:
            max_station_list[1].append[station]
    return max_station_list


print(get_max_bus_stops(get_metro_exits(file_name_metro,enc), get_bus_stops(file_name_bus, enc)))
