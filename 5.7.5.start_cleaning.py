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
    аремя отработки функций выводить
    описать, что принимает на вход.
    передача радиуса и округления внутрь.
    сократить один if with and
'''

from csv import reader
from datetime import datetime
from json import loads
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
    
    # Достаём из списка автобусов максимальное и 
    # минимальное значение широты для получения
    # границ кол-ва метров на градус долготы. Список 
    # отсортированный, поэтому достаточно двух крайних 
    # элементов. Сравниваем значения по модулю, чтобы
    # работало и в южном полушарии. Исходим из предположения
    # что охват автобусными остановками шире охвата метро
    # по соображениям экономики (т.е. покрывается 
    # вся исследуемая область).
    #
    # Как быстро достать первый и последний элементы сета?
    # ? next(iter(bus)) - должен достать первый
    bus_lat_list = [lat for lat, lon in bus]
    if abs(bus_lat_list[0]) > abs(bus_lat_list[-1]):
        max_bus_lat = bus_lat_list[0]
        min_bus_lat = bus_lat_list[-1]
    else:
        max_bus_lat = bus_lat_list[-1]
        min_bus_lat = bus_lat_list[0]
    # Получаем нижнее значение градус / метр в исследуемой
    # области (ближе к экватору). Уменьшаем для верности.
    # Т.е. получаем такую часть градуса долготы, которая 
    # гарантированно будет меньше метра.
    # Аналогично верхнее значение и верхний долготный радиус.
    lower_lon_m = (1 / distance((min_bus_lat, 0), (min_bus_lat, 1)).m) * (1 - rounding)
    upper_lon_m = (1 / distance((max_bus_lat, 0), (max_bus_lat, 1)).m) * (1 + rounding)
    upper_lon_rad = radius * upper_lon_m
    # Подобным образом получаем значение градуса широты,
    # которое меньше метра. Пределы на земле: 110574м/градус,
    # 111699м/градус. Чуть раздвигаю пределы для верности.
    # Аналогично верхнее значение и верхний широтный радиус.
    lower_lat_m = 1 / 111700
    upper_lat_m = 1 / 110500
    upper_lat_rad = radius * upper_lat_m
    # Результат в виде макс. кол-ва остановок и списка станций,
    # если таких больше одной.
    result = [0, []]
    # Сбрасываемый для каждой станции список удовлетворяющих
    # остановок, чтобы не считать их многократно. Остановка
    # может быть в радиусе нескольких выходов.
    counted_for_station = set()

    for station, station_coord_list in metro.items():
        # Счётчик удовлетворяющих остановок для станции.
        counter = 0
        # Находим макс. и мин. широты для выходов.
        metro_lat_list = [lat for lat, lon in station_coord_list]
        min_metro_lat = min(metro_lat_list)
        max_metro_lat = max(metro_lat_list)
        # Для ускорения для каждой станции создаётся 
        # уменьшенный набор координат остановок. В нём 
        # будут только остановки в диапазоне широт чуть шире
        # "radius" от выходов из метро.
        # Получаем "полосу" вдоль параллели.
        bus_reduced = set()
        # Набор "bus" отсортирован по широте. Доходим до нижней границы
        # широт, в которых находятся интересующие остановки.
        # Помещаем их в набор, как только доходим до верхней 
        # границы - прекращаем.
        for lat, lon in bus:
            if lat >= min_metro_lat - upper_lat_rad:
                if lat <= max_metro_lat + upper_lat_rad:
                    bus_reduced.add((lat, lon))
                else:
                    break
        for station_exit in station_coord_list:
            # Распаковываем для скорости координаты
            # выхода.
            exit_lat, exit_lon = station_exit
            for bus_stop in bus_reduced:
                bus_lat, bus_lon = bus_stop
                # TODO: порядок поменять вокруг "and"
                # Отсекаем уже подсчитанные остановки и
                # те, что дальше "radius" по долготе.
                # Т.е. отсекаем края "полосы" вдоль меридиана,
                # сокращая искомую область до "квадрата".
                if (abs(bus_lon - exit_lon) < upper_lon_rad
                        and bus_stop not in counted_for_station):
                    # Далее уже описываем окружности вокруг станции.
                    # Всё что дальше чуть больше "radius" нас не интересует.
                    # Отсекаем "углы" "квадрата".
                    if hypot(((bus_lat - exit_lat) / upper_lat_m),
                             ((bus_lon - exit_lon) / upper_lon_m)) > radius:
                        continue
                    # Если остановка ближе "radius" - гарантированно наша.
                    # Остаётся "кольцо" координат остановок, которые могут 
                    # быть искомыми. Их проверяем точным и дорогим алгоритмом
                    # Винсенти.
                    elif hypot(((bus_lat - exit_lat) / lower_lat_m), ((bus_lon - exit_lon) / lower_lon_m)) < radius or distance(bus_stop, station_exit).m <= radius:
                        # Остановка найдена, добавляем в список посчитанных
                        # для этой станции. Прибавляем счётчик остановок.
                        counted_for_station.add(bus_stop)
                        counter += 1
        # Для следующей станции заполняем список заново.
        counted_for_station.clear()
        # Если это чемпион по кол-ву остановок, то перезаписываем 
        # результат. Если такое кол-во уже было у других станций, то
        # добавляем название станции.
        if counter > result[0]:
            result.clear()
            result.extend([counter, [
                station,
            ]])
        elif counter == result[0]:
            result[1].append(station)
    # Всё посчитано, форматируем вывод.
    fresult = 'В радиусе {} {} от выходов из метро больше всего автобусных остановок ({}) на {} метро {}.'.format(
        radius, 'метра' if radius == 1 else 'метров', result[0], 'станциях'
        if len(result[1]) > 1 else 'станции', ', '.join(sorted(result[1])))

    return fresult


bus_stops = get_bus_stops(file_name_bus, enc, delim)
metro_exits = get_metro_exits(file_name_metro, enc)
w1 = datetime.now()
max_bus_stop = get_max_bus_stops(metro_exits, bus_stops)
print(max_bus_stop, datetime.now() - w1)
