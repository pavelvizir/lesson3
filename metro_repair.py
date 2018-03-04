import json
from datetime import datetime  #, timedelta date, 
file_name='data-397-2018-02-27.json'
enc = 'windows-1251'
#enc = 'utf-8'
today = datetime.today()
with open(file_name, 'r', encoding=enc) as file:
	reader = json.loads(file.read())
#	i = 1 
	d = set()
	for line in reader:
		#print(line)
		#if i < 5000:
			#print(line.keys())
			#if line['RepairOfEscalators']:
			for a in line['RepairOfEscalators']:
					#a = line.get('RepairOfEscalators')
					#if not a:
					#print(line)
					#continue

					#else:
				if a:
					b = a['RepairOfEscalators'].split('-')
				#print(b)
				#strptime(b[0], '%d.%m.%Y')
					if datetime.strptime(b[0], '%d.%m.%Y') <= today <= datetime.strptime(b[1], '%d.%m.%Y'):
					#print(line['NameOfStation'], b)
						d.add(line['NameOfStation'])

			#else:
			#	print(line['RepairOfEscalators'])
			#	print(i)
				#

		#	i+=1
			#print(line.keys())
		#else:
		#	break
	#print(reader)
	# for line in file:
	# 	json.loads(line)

	print(sorted(d))