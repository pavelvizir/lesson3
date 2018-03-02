import csv

answers = {"привет": "И тебе привет!",
           "как дела": "Лучше всех!",
           "пока": "Увидимся."}
file = 'csv_result.csv'
with open(file, 'w', encoding    =    'utf-8') as f:
    fields =    ['ключ', 'значение']
    writer =    csv.DictWriter(f, fields, delimiter =    ';')
    writer.writeheader()
    writer.writerows([{fields[0]:a, fields[1]: b}    for a,b in answers.items()])
        
with open(file,'r', encoding =    'utf-8') as g:
    fields =    ['ключ', 'значение']
    writer =    csv.DictReader(g, fields, delimiter =    ';')
    for line in g:
        print(line)