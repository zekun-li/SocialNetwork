#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
import re

#guardian = open('guardian_peruser.json','r')
#guardian_comments = json.load(guardian)

nytimes = open('nytimes_peruser.json','r')
nytimes_comments = json.load(nytimes)

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

nytimes_active_user_comment={}
for name in nytimes_active_user:
	nytimes_active_user_comment[name] ={}
	nytimes_active_user_comment[name]['totalcount'] = 0
	nytimes_active_user_comment[name]['reussiscount'] = 0

guardian_active_user_comment={}
for name in guardian_active_user:
	guardian_active_user_comment[name] ={}
	guardian_active_user_comment[name]['totalcount'] = 0
	guardian_active_user_comment[name]['reussiscount'] = 0

counter = 0
for comment in nytimes_comments:

	counter += 1
	#if counter % 1000 == 0:
	#	print counter

	name = comment['author_name']
	name = name.encode('utf8').strip()  if type(name) != type(1) else str(name)
	if name in nytimes_active_user:
		nytimes_active_user_comment[name]['totalcount'] += 1

		text = comment['text'].encode('ascii',errors='ignore')
		text = text.replace('<br/>','.')
		text = text.replace('\n',' ')
		text = re.sub('[/"¨”´’{}[+^=*$%_`~#|\]]','',text)
		#text = re.sub('[<>(),.:\';!?&]',' ',text)
		
		words = text.lower().split()
		if 'putin' in words or 'putin\'s' in words or 'russia' in words or 'ukraine' in words or 'crimea' in words or 'russia\'s' in words:
			nytimes_active_user_comment[name]['reussiscount'] += 1
'''counter = 0
for comment in guardian_comments:
	counter += 1
	#if counter % 1000 == 0:
	#	print counter

	name = comment['author_name']
	name = name.encode('utf8').strip()  if type(name) != type(1) else str(name)
	if name in guardian_active_user:
		guardian_active_user_comment[name]['totalcount'] += 1

		text = comment['text'].encode('ascii',errors='ignore')
		text = text.replace('<br/>','.')
		text = text.replace('\n',' ')
		text = re.sub('[/"¨”´’{}[+^=*$%_`~#|\]]','',text)
		#text = re.sub('[<>(),.:\';!?&]',' ',text)
		
		words = text.lower().split()
		if 'putin' in words or 'putin\'s' in words or 'russia' in words or 'ukraine' in words or 'crimea' in words or 'russia\'s' in words:
			guardian_active_user_comment[name]['reussiscount'] += 1'''


#print guardian_active_user_comment

for name in nytimes_active_user_comment:
	if nytimes_active_user_comment[name]['totalcount'] != 0: 
		if  nytimes_active_user_comment[name]['totalcount'] >=10 and nytimes_active_user_comment[name]['reussiscount']*1.0/nytimes_active_user_comment[name]['totalcount'] > 0.8:
			print name,nytimes_active_user_comment[name]['totalcount'],nytimes_active_user_comment[name]['reussiscount']*1.0/nytimes_active_user_comment[name]['totalcount']


'''for name in guardian_active_user_comment:
	if guardian_active_user_comment[name]['totalcount'] != 0: 

		if  guardian_active_user_comment[name]['totalcount'] >=10 and guardian_active_user_comment[name]['reussiscount']*1.0/guardian_active_user_comment[name]['totalcount'] > 0.8:
			print name,guardian_active_user_comment[name]['totalcount'],guardian_active_user_comment[name]['reussiscount']*1.0/guardian_active_user_comment[name]['totalcount']'''
