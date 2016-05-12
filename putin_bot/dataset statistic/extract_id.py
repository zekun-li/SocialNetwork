#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import pickle

nytimes = open('nytimes_comments.json','r')
nytimes_comments = json.load(nytimes)

guardian = open('guardian_comments.json','r')
guardian_comments = json.load(guardian)

active_user = open('active_users.txt','r')
nytimes_active_user = []
guardian_active_user = []

def get_screen_name(line):
	name_list = line.split()
	length = len(name_list[0]) + len(name_list[1]) + len(name_list[2]) + 3

	return line[length:].strip()


for line in active_user:
	if line.split()[0] == 'nytimes':
		nytimes_active_user.append(get_screen_name(line))
	elif line.split()[0] == 'guardian':
		guardian_active_user.append(get_screen_name(line))

nytimes_name_id_dict = {}
guardian_name_id_dict = {}

for comment in nytimes_comments:
	name = comment['author_name']
	name = name.encode('utf8').strip()  if type(name) != type(1) else str(name)
	if name in nytimes_active_user:
		id = int(comment['author_id'])
		if name not in nytimes_name_id_dict:
			nytimes_name_id_dict[name] = []
			nytimes_name_id_dict[name].append(id)
		else:
			if id not in nytimes_name_id_dict[name]:
				nytimes_name_id_dict[name].append(id)

for comment in guardian_comments:
	name = comment['author_name']
	name = name.encode('utf8').strip()  if type(name) != type(1) else str(name)
	if name in guardian_active_user:
		id = int(comment['author_id'])

		if name not in guardian_name_id_dict:
			guardian_name_id_dict[name] = []
			guardian_name_id_dict[name].append(id)
		else:
			if id not in guardian_name_id_dict[name]:
				guardian_name_id_dict[name].append(id)
print guardian_name_id_dict

pickle.dump(nytimes_name_id_dict, open("nytimes_name_id_dict.p", "wb")) 
pickle.dump(guardian_name_id_dict, open("guardian_name_id_dict.p", "wb")) 
