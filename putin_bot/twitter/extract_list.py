#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json


def get_screen_name(line):
	name_list = line.split()[0:-2]

	if len(name_list) == 1:
		return name_list[0]
	else:
		name = ''
		for i in range(len(name_list)):
			name = name + name_list[i]
			if i < len(name_list) - 1:
				name = name + ' '
		return name


def get_screen_name_2(line):
	name_list = line.split()[3:]

	if len(name_list) == 1:
		return name_list[0]
	else:
		name = ''
		for i in range(len(name_list)):
			name = name + name_list[i]
			if i < len(name_list) - 1:
				name = name + ' '
		return name

guardian_active_user_list = {}
nytimes_active_user_list = {}

guardian_cluster_file = open('guardian_active_users_cluster.txt','r')
for line in guardian_cluster_file:
	name =  get_screen_name(line)
	guardian_active_user_list[name] = line.split()[-2:-1][0]

nytimes_cluster_file = open('nytimes_active_users_cluster.txt','r')
for line in nytimes_cluster_file:
	name =  get_screen_name(line)
	nytimes_active_user_list[name] = line.split()[-2:-1][0]

cross_twitter_file = open('user_name_twitter_crossreference.txt','r').readlines()
user_file = open('users.txt','r').readlines()

outfile = open('matching_twitter_user_with_cluster.txt','w+')
for i in range(len(cross_twitter_file)):
	if cross_twitter_file[i].split()[-1] == 'Hit':
		label = True
	else:
		label = False

	if label:
		name = get_screen_name_2(user_file[i])
		if user_file[i].split()[0] == 'guardian':
			if name in guardian_active_user_list:
				outfile.write( cross_twitter_file[i].split()[0] + ' ' + guardian_active_user_list[name] + '\n')

		elif user_file[i].split()[0] == 'nytimes':
			if name in nytimes_active_user_list:
				outfile.write(  cross_twitter_file[i].split()[0] + ' ' + nytimes_active_user_list[name] + '\n')
