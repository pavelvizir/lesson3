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
from random import choice, sample


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


def get_max_bus_stops_slow(bus, metro, radius):
    ''' Возвращает максимальное количество остановок
        и список станций в отформатированном виде.
        Работает медленно.'''
    result = [0, []]
    counted_for_station = set()
    for station, station_coord_list in metro.items():
        counter = 0
        for station_exit in station_coord_list:
            for bus_stop in bus:
                if bus_stop not in counted_for_station\
                            and distance(bus_stop, station_exit).m <= radius:
                    counted_for_station.add(bus_stop)
                    counter += 1
        counted_for_station.clear()
        if counter > result[0]:
            result.clear()
            result.extend([counter, [station, ]])
        elif counter == result[0]:
            result[1].append(station)
    text_result = '''В радиусе {} {} от выходов из метро больше всего автобусных\
 остановок ({}) на {} метро {}.'''.format(
     radius,
     'метра' if radius == 1 else 'метров',
     result[0],
     'станции' if not len(result[1]) > 1 else 'станциях',
     ', '.join(sorted(result[1])))

    return text_result


def get_max_bus_stops_fast(bus, metro, radius, rounding):
    ''' Возвращает максимальное количество остановок
        и список станций в отформатированном виде. '''
    # Результат в виде макс. кол-ва остановок и списка станций,
    # если таких больше одной.
    result = [0, []]
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
    lower_lon_m = (1 / distance((min_bus_lat, 0), (min_bus_lat, 1)).m)\
        * (1 - rounding)
    upper_lon_m = (1 / distance((max_bus_lat, 0), (max_bus_lat, 1)).m)\
        * (1 + rounding)
    upper_lon_rad = radius * upper_lon_m
    # Подобным образом получаем значение градуса широты,
    # которое меньше метра. Пределы на земле: 110574м/градус,
    # 111699м/градус. Чуть раздвигаю пределы для верности.
    # Аналогично верхнее значение и верхний широтный радиус.
    lower_lat_m = 1 / 111700
    upper_lat_m = 1 / 110500
    upper_lat_rad = radius * upper_lat_m
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
            # Распаковываем координаты выхода для скорости.
            exit_lat, exit_lon = station_exit
            for bus_stop in bus_reduced:
                bus_lat, bus_lon = bus_stop
                # Отсекаем уже подсчитанные остановки и
                # те, что дальше "radius" по долготе.
                # Т.е. отсекаем края "полосы" вдоль меридиана,
                # сокращая искомую область до "квадрата".
                if (bus_stop not in counted_for_station
                        and abs(bus_lon - exit_lon) < upper_lon_rad):
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
                    elif radius > hypot(((bus_lat - exit_lat) / lower_lat_m),
                                        ((bus_lon - exit_lon) / lower_lon_m))\
                            or distance(bus_stop, station_exit).m <= radius:
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
            result.extend([counter, [station, ]])
        elif counter == result[0]:
            result[1].append(station)
    # Всё посчитано, форматируем вывод.
    text_result = '''В радиусе {} {} от выходов из метро больше всего автобусных\
 остановок ({}) на {} метро {}.'''.format(
     radius,
     'метра' if radius == 1 else 'метров',
     result[0],
     'станции' if not len(result[1]) > 1 else 'станциях',
     ', '.join(sorted(result[1])))

    return text_result


def load_data(file_bus, file_metro, encoding, delimiter):
    ''' Загружает информацию из файлов. '''
    time_1 = datetime.now()
    bus = get_bus_stops(file_bus, encoding, delimiter)
    time_2 = datetime.now()
    metro = get_metro_exits(file_metro, encoding)
    time_3 = datetime.now()
    # Не хочу пока обрабатывать ошибки. Предположим, что всё всегда ок.
    result = '\n'.join([
        'Data loading complete.\n Time taken:',
        '\t{:10}{}'.format("Bus:", time_2 - time_1),
        '\t{:10}{}'.format("Metro:", time_3 - time_2),
        '\t{:10}{}\n'.format("Total:", time_3 - time_1)])

    return bus, metro, result


def get_max_bus_stops_wrapper(bus, metro, rounding, mode, radius=None):
    ''' Запускает нужную функцию или тест. '''
    radius = radius or 500  # Начальная постановка задачи
    if mode == 'fast':
        time_1 = datetime.now()
        result = get_max_bus_stops_fast(bus, metro, radius, rounding)
        result += '\n Time taken: {}\n'.format(datetime.now() - time_1)
    elif mode == 'slow':
        time_1 = datetime.now()
        result = get_max_bus_stops_slow(bus, metro, radius)
        result += '\n Time taken: {}\n'.format(datetime.now() - time_1)
    elif mode == 'test':
        metro_reduced = {k: metro[k] for k in sample(list(metro.keys()), 2)}
        time_1 = datetime.now()
        result_fast = get_max_bus_stops_fast(bus, metro_reduced, radius, rounding)
        time_2 = datetime.now()
        result_slow = get_max_bus_stops_slow(bus, metro_reduced, radius)
        time_3 = datetime.now()
        if result_fast == result_slow:
            result = 'Test passed.\nStations were: {}\n{}'.format(', '.join(metro_reduced), result_fast)
        else:
            result = 'Test failed.\nStations were: {}\n Results were:\n\t\
                    Fast:\n\t{}\nSlow:\n\t{}'.format(', '.join(metro_reduced), result_fast, result_slow)
        result += '\n'.join([
            '\n Time taken:',
            '\t{:10}{}'.format('Fast:', time_2 - time_1),
            '\t{:10}{}'.format('Slow:', time_3 - time_2),
            '\t{:10}{}'.format('Total:', time_3 - time_1),
            '\t{:16}{}\n'.format('Rate:', int((time_3 - time_2)/(time_2-time_1)))])

    else:
        result = 'Unknown mode. Doing nothing.'

    return result


if __name__ == "__main__":
    file_name_bus = 'data-398-2018-02-13.csv'
    file_name_metro = 'data-397-2018-02-27.json'
    enc = 'windows-1251'
    delim = ';'
    rounding = 0.001
    bus_stops, metro_exits, load_data_result =\
        load_data(file_name_bus, file_name_metro, enc, delim)
    print(load_data_result)
    print(get_max_bus_stops_wrapper(bus_stops, metro_exits, rounding, 'fast', 1000))
    print(get_max_bus_stops_wrapper(bus_stops, metro_exits, rounding, 'test', 1000))
    for i in range(20):
        print(get_max_bus_stops_wrapper(bus_stops, metro_exits, rounding, 'test', 1000))

