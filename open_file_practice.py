''' TODO: regexp with more delimeters.
'''
def count_words_in_file (file):
	with open(file,'r',encoding='utf-8') as f:
		text =	f.read()
		return 'File {} has {} words.'.format(file, len(text.split()))
		
print(count_words_in_file('referat.txt'))