'''
Остановки у метро
Объединить наборы данных из предыдущих задач и посчитать,
 у какой станции метро больше всего остановок (в радиусе 0.5 км).

'''

import csv
file_name = 'data-398-2018-02-13.csv'
delim = ';'
enc = 'windows-1251'
#enc = 'utf-8'
with open(file_name, 'r', encoding=enc) as file:
	reader = csv.reader(file, delimiter=delim)
	d = {}
	for line in reader:
			if line[4] in d:
				d[line[4]] += 1
			else:
				d[line[4]] = 1
	d.pop('Street')
	d_inverted = {v: k for k, v in d.items()}
	print(len(d), sum(d.values()), d_inverted[max(d.values())])
# from collections import Counter

# ...
# streets = [row['Street'] for row in reader]
# print(Counter(streets).most_common(1))