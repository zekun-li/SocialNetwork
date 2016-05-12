#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import datetime 

guardian = open('guardian_comments.json','r')
guardian_comments = json.load(guardian)

nytimes = open('nytimes_comments.json','r')
nytimes_comments = json.load(nytimes)

user_file = open('users.txt','w+')
active_user_file = open('active_users.txt','w+')
overlap_file = open('guardian_nytimes_overlap_users.txt','w+')

guardian_user_dict = {}
nytimes_user_dict = {}
guardian_article = []
nytimes_article = []
active_guardian_user_id = []
active_nytimes_user_id = []
guardian_reply_count = 0
nytimes_reply_count = 0

guardian_lower_timestamp = float('inf')
guardian_upper_timestamp =  0
nytimes_lower_timestamp =  float('inf')
nytimes_upper_timestamp =  0

counter = 0
for comment in guardian_comments:

	timestamp = int(comment['date_js_timestamp'][:-3])
	if timestamp < guardian_lower_timestamp:
		guardian_lower_timestamp = timestamp
	if timestamp > guardian_upper_timestamp:
		guardian_upper_timestamp = timestamp
	
	if comment['article'] not in guardian_article:
		guardian_article.append(comment['article'])

	if comment['reply_comment_id'] != "":
		guardian_reply_count +=1

	name = comment['author_name']
	name = name.encode('utf8')  if type(name) != type(1) else str(name)

	if name not in guardian_user_dict:
		guardian_user_dict[name] = {}
		guardian_user_dict[name]['NumberOfComment'] = 1
		guardian_user_dict[name]['NumberOfReply'] = 0
	else:
		guardian_user_dict[name]['NumberOfComment'] += 1

	if comment['reply_user_name'] != "":
		reply_name = comment['reply_user_name']
		reply_name = reply_name.encode('utf8')  if type(reply_name) != type(1) else str(reply_name)
		if reply_name not in guardian_user_dict:
			guardian_user_dict[reply_name] = {}
			guardian_user_dict[reply_name]['NumberOfComment'] = 0
			guardian_user_dict[reply_name]['NumberOfReply'] = 1
		else:
			guardian_user_dict[reply_name]['NumberOfReply'] += 1

	counter += 1
	if counter % 10000 == 0:
		print counter

for comment in nytimes_comments:
	timestamp = int(comment['date_js_timestamp'])
	if timestamp < nytimes_lower_timestamp:
		nytimes_lower_timestamp = timestamp
	if timestamp > nytimes_upper_timestamp:
		nytimes_upper_timestamp = timestamp

	if comment['article'] not in nytimes_article:
		nytimes_article.append(comment['article'])

	if comment['reply_comment_id'] != "":
		nytimes_reply_count +=1

	name = comment['author_name']
	name = name.encode('utf8')  if type(name) != type(1) else str(name)

	if name not in nytimes_user_dict:
		nytimes_user_dict[name] = {}
		nytimes_user_dict[name]['NumberOfComment'] = 1
		nytimes_user_dict[name]['NumberOfReply'] = 0
	else:
		nytimes_user_dict[name]['NumberOfComment'] += 1

	if comment['reply_user_name'] != "":
		reply_name = comment['reply_user_name']
		reply_name = reply_name.encode('utf8')  if type(reply_name) != type(1) else str(reply_name)
		if reply_name not in nytimes_user_dict:
			nytimes_user_dict[reply_name] = {}
			nytimes_user_dict[reply_name]['NumberOfComment'] = 0
			nytimes_user_dict[reply_name]['NumberOfReply'] = 1
		else:
			nytimes_user_dict[reply_name]['NumberOfReply'] += 1
	
	counter += 1
	if counter % 10000 == 0:
		print counter


guardian_name_list = []
nytimes_name_list = []

user_file.write('dataset #comments #reply name \n')
active_user_file.write('dataset #comments #reply name \n')
for name in guardian_user_dict:
	user_file.write('guardian ' + str(guardian_user_dict[name]['NumberOfComment']) + ' ' + str(guardian_user_dict[name]['NumberOfReply']) + ' ' + str(name) + ' \n')

	if name not in guardian_name_list:
		guardian_name_list.append(name)
	if guardian_user_dict[name]['NumberOfComment'] >= 10:
		active_guardian_user_id.append(name)
		active_user_file.write('guardian ' + str(guardian_user_dict[name]['NumberOfComment']) + ' ' + str(guardian_user_dict[name]['NumberOfReply']) + ' ' + str(name) + ' \n')

for name in nytimes_user_dict:
	user_file.write('nytimes ' + str(nytimes_user_dict[name]['NumberOfComment']) + ' ' + str(nytimes_user_dict[name]['NumberOfReply']) + ' ' + str(name) + ' \n')

	if name not in nytimes_name_list:
		nytimes_name_list.append(name)
	if nytimes_user_dict[name]['NumberOfComment'] >= 10:
		active_nytimes_user_id.append(name)
		active_user_file.write('nytimes ' + str(nytimes_user_dict[name]['NumberOfComment']) + ' ' + str(nytimes_user_dict[name]['NumberOfReply']) + ' ' + str(name) + ' \n')

print('number of reply in guardian dataset: ' + str(guardian_reply_count) + '\n')
print('number of reply in nytimes dataset: ' + str(nytimes_reply_count) + '\n')
print('number of users in guardian dataset: ' + str(len(guardian_user_dict)) + '\n')
print('number of users in nytimes dataset: ' + str(len(nytimes_user_dict)) + '\n')
print('number of active users in guardian dataset: ' + str(len(active_guardian_user_id)) + '\n')
print('number of active users in nytimes dataset: ' + str(len(active_nytimes_user_id)) + '\n')
print('number of articles in guardian dataset: ' + str(len(guardian_article)) + '\n')
print('number of articels in nytimes dataset: ' + str(len(nytimes_article)) + '\n')

dt = datetime.datetime.fromtimestamp(guardian_lower_timestamp)
print dt.strftime('%d %b %Y %H:%M')
dt = datetime.datetime.fromtimestamp(guardian_upper_timestamp)
print dt.strftime('%d %b %Y %H:%M')

dt = datetime.datetime.fromtimestamp(nytimes_lower_timestamp)
print dt.strftime('%d %b %Y %H:%M')
dt = datetime.datetime.fromtimestamp(nytimes_upper_timestamp)
print dt.strftime('%d %b %Y %H:%M')

print ('Overlapping bewtween two datasets\' user_name:')
print not frozenset(guardian_name_list).isdisjoint(frozenset(nytimes_name_list))

overlap = set(guardian_name_list).intersection(nytimes_name_list)
print('overlapping user name: ' + str(len(overlap)))
print overlap

counter = 0
for name in overlap:
	if name in active_nytimes_user_id or name in active_guardian_user_id:
		counter += 1

	overlap_file.write(str(name) + '\n')

print counter
