# -*- coding: utf-8 -*- 
import re
import csv
import sys
import json
import pickle


# -------------------------------- get top users id -----------
topusers = set()
f = open('../data/user_graph_d7w7.csv','r')
csv_f = csv.reader(f)
next(csv_f)

for row in csv_f:
	user_id = row[1] # get user id
	topusers.add(user_id)
print 'Number of top users:'
print len(topusers)

# ----------------------------- create user_comment table ------
with open('../data/guardian_comments.json') as data_file:    
    rawInfo = json.load(data_file)

csvfile = open('../data/user_comment_table.csv', 'wb')
csv_writer = csv.writer(csvfile)

user_comment_table={}
ct = 0
for ind in range(0, len(rawInfo)):
	ct += 1
	record = rawInfo[ind]
	authorId = record['author_id']  
	if authorId in topusers:
		comment = record['text'].encode('ascii',errors='ignore')
		comment = comment.replace('<br/>','.')
		comment = comment.replace('\n',' ')
		comment = re.sub('[/"¨”´’{}[+^=*$%_`~#|\]]','',comment)

		#words = comment.lower().split()
		#if 'putin' in words or 'putin\'s' in words:
		if authorId not in user_comment_table:
			user_comment_table[authorId] = []
		else:
			user_comment_table[authorId].append(comment.strip())

for key, value in user_comment_table.items():
	csv_writer.writerow([key, value])