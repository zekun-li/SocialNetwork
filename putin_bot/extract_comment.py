#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import re
import pickle
import csv

csvfile = open('nytimes_less_comments.csv', 'wb')
csv_writer = csv.writer(csvfile)

def get_screen_name(line):
	name_list = line.split()
	length = len(name_list[0]) + len(name_list[1]) + len(name_list[2]) + 3

	return line[length:].strip()

guardian_user_list = []
nytimes_user_list = []

user_file = open('active_users.txt','r')
for line in user_file:
	if line.split()[0] == 'nytimes':
		nytimes_user_list.append(get_screen_name(line))
	elif line.split()[0] == 'guardian':
		guardian_user_list.append(get_screen_name(line))
user_file.close()

nytimes = open('nytimes_comments.json','r')
nytimes_comments = json.load(nytimes)
nytimes.close()


name_comment_dict = {}
for name in nytimes_user_list:
	name_comment_dict[name] = []

counter = 0
comment_counter = 0
for comment in nytimes_comments:
	counter += 1
	if counter % 1000 == 0:
		print counter
	
	name = comment['author_name']
	name = name.encode('utf8').strip()  if type(name) != type(1) else str(name)	
	if name in nytimes_user_list:
		text = comment['text'].encode('ascii',errors='ignore')
		text = text.replace('<br/>','.')
		text = text.replace('\n',' ')
		text = re.sub('[/"¨”´’{}[+^=*$%_`~#|\]]','',text)
		#text = re.sub('[<>(),.:\';!?&]',' ',text)
		
		words = text.lower().split()
		if 'putin' in words or 'putin\'s' in words:
			if len(name_comment_dict[name]) <10:
				comment_counter += 1
				name_comment_dict[name].append(text.strip())
				csv_writer.writerow([name,text])
	else:
		continue

pickle.dump( name_comment_dict, open("name_comment_dict.p", "wb")) 
print comment_counter


for name in name_comment_dict:
	if len(name_comment_dict[name]) == 0:
		print name
