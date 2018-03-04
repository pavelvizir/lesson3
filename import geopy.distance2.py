import geopy.distance, csv, json
from math import sqrt

coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)

#print geopy.distance.vincenty(coords_1, coords_2).km
#geopy.distance.VincentyDistance(coords_1, coords_2).km
file_name_bus = 'data-398-2018-02-13.csv'
delim = ';'
enc = 'windows-1251'
with open(file_name_bus, 'r', encoding=enc) as file:
	reader = csv.reader(file, delimiter=delim)
	bus_coord = {}
	for line in reader:
			bus_coord[line[0]] = (line[2], line[3])

	bus_coord.pop('ID')
	print(len(bus_coord), bus_coord['65'])


file_name_metro='data-397-2018-02-27.json'
with open(file_name_metro, 'r', encoding=enc) as file:
	reader = json.loads(file.read())
	metro_coord = {}
	i = 1
	for line in reader:
		if i < 200:
	#		print(line)
	#		print(line['geoData']['coordinates'])
	#		print(line['NameOfStation'])
#			if not metro_coord[line['NameOfStation']]:
#				metro_coord[line['NameOfStation']] = [(line['geoData']['coordinates'][0], line['geoData']['coordinates'][1]),]
#			else:
			try:
				metro_coord[line['NameOfStation']].append((line['geoData']['coordinates'][0], line['geoData']['coordinates'][1]))
			except KeyError:
				metro_coord[line['NameOfStation']] = [(line['geoData']['coordinates'][0], line['geoData']['coordinates'][1]),]

		else:
			break

		i+=1

a = []
for station, coord_list in metro_coord.items():
	for bus_stop_id, bus_stop_coord in bus_coord.items():
		if sqrt((coord_list[0][0] - float(bus_stop_coord[0]))**2 + (coord_list[0][1] - float(bus_stop_coord[1]))**2) < 0.006
	for exit in coord_list:
		print(station, exit)
		for bus_stop_id, bus_stop_coord in bus_coord.items():
#		for bus_stop_id, bus_stop_coord in bus_coord.items():
			if sqrt((exit[0] - float(bus_stop_coord[0]))**2 + (exit[1] - float(bus_stop_coord[1]))**2) < 0.006:
				if geopy.distance.VincentyDistance(bus_stop_coord, exit).m <= 500:
					#print(bus_stop_coord)
					#print(sqrt((exit[0] - float(bus_stop_coord[0]))**2 + (exit[1] - float(bus_stop_coord[1]))**2))
					#print(geopy.distance.VincentyDistance(bus_stop_coord, exit).m)
					#print(bus_stop_id)
					a.append(bus_stop_id)
	#				del bus_coord[bus_stop_id]
	#				pass
			
		for b in a:
			del bus_coord[b]

		a.clear()


	print(len(bus_coord))

print(len(bus_coord))	
#	print(geopy.distance.VincentyDistance(bus_coord['65'], metro_coord[]).km)
# 			for a in line['RepairOfEscalators']:
# 				if a:
# 					b = a['RepairOfEscalators'].split('-')
# 					if datetime.strptime(b[0], '%d.%m.%Y') <= today <= datetime.strptime(b[1], '%d.%m.%Y'):
# 						d.add(line['NameOfStation'])
# 	print(sorted(d))