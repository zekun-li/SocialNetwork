#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import json
from twython import Twython,TwythonError
import os
import re
import pickle

def get_screen_name(line):
	name_list = line.split()[3:]

	if len(name_list) == 1:
		return name_list[0]
	else:
		name = ''
		for i in range(len(name_list)):
			name = name + name_list[i]

		return name

APP_KEY_list = ['OtfN9Y44IwLAHBKMv71RetkI9','A23vttrQZ1DfiJ3pmuDGhPD4y','nYISFdad9Uda0G1664e9oYIbB','ey2hjuNPKF8wRUH3vd93iE0Mt','9SoyWbxA07doZkeUHDycbHUKt','zfTMAAT05iTcK1wVlDUe6Pbxm','IhJZomBHoITioZDFFKUt56k6h','UMRzJbkAws2GkPcoz7cxUDex4','KOg6W3ML7SwjKTjTcMUjsVJ1I','qM1aC0CxNDXSV7RyQJROixBz1','dW2k0kxz6KdSsSEdv6TluP6Vn','PZUyTiZ0jXJhMAlA1fjOuF03j','QfUSiHvyibOYiwD9vCWSK68WK','g4n2lOFbVZmjEs5dVTkgCUf9e','4dSrciDxq2EpdWEDSElN3iHh4','aA6dtRUJqdBPBUFKsDNNht77c','YQFamiykFGKhXVwHSp1cuAP7t','d9eYbOpnqWwo9CSVaSGk27FA7','8wM4LWaC59DV2yNCe8zMUIaLz','lp8jwJrb3Cxtf8eejll9vg1Tb','SyFM7SgSC2dKdsks1cY7P5Fnc','D1xPx6TROqJTjWpWLzQNKmpIO','Tk6dGwBIFyv3H17EHPFKMDYj8','EjonFXsVnSmh0fxmpcvJJG1wm','vqw2rJ0w9tjr9JOemhOXAseMh','uJFDF0dBcFbzHA1TswbpOvAAW','cYW8yzBDTzLLq41XgSzdkCDKH','9CcXGdNjn4BBCwu088YxQCbkW']
APP_SECRET_list = ['3UwhgtMhGhk1ZFwbBAqt57TMVfxJlPiWvIhTTV0iWCQdHe4CkY','f5cye1bX9LyBPdcIkC6f9yPMc2VGWMRUZTsrd7ArQLnffk0dL6','84y3UhGQjB5bpXpG2T5ftBCu0iWfq4Yclnr3UthONLkDib5UxB','ZC61IYwzi8GR2Ts0xQ0EVJekArAWrWZ5kjRMOOfdaB1NjsoZZe','ZGs9gsnqw0Ch2OxXWhMYqICtCnw9OAh3SFBNtr2ZmPpr07UTBX','XZO13kNFN4XO56V3uFZl6t9nqhI2Orp4SFzgiDIzwQ82I6PzRE','km33WpTT12imiq9ApnCCfSbA0X6q4bffXiatyf2bKLbv5tqnid','uXwdYs85p7JZG1lYrDi7uINufXTDIwF4lztJWss1F7v0qFYzd4','lemiWVZLWtvLeozut4RA92dgLBBUq1nYEPOQCBbXPWfwG1D5jw','hQVPODJavXvm0xt9zS8MZMTkyarxEIjkPpi0GlWzp6da73gAl4','uOrUJvfDpwRdFCVGFwT7hzQiWGbgDoOpF8lZnSV5JlbMO1qCjq','gHBeap9YBYXER1aZbdpCD0pSMxtPBFDBefnePisZg84n0p7LOy','IKRv5cWkbaHLsn9z1keBX6znQ6Jj9KQHwV5frycrAh72b1U2T8','tZb8ZQeE0PpYKHGQjD1xahomE4coPlNPAkaLaqkg6Ikn2RGGfL','g6RMC9DUZssVVBFyI1DcbALQn8H8mwGOYd9ZZiKlZEZVQOu4gh','fyzLTE5Wr7z0jt1N3Csfalhg6QF8EKJApG8yNjTSWCPlD1vd1r','8ZdyCFOT7mNNs6kHQHTjz655jcvktmEzQWNi2Jjl2MLfw3nu0e','JshzipSq4kPKiZ3aP0CU5naUBrsGgzbdNFivXns7JTBdD0QPAr','YbThXI8xbe680u2aDia7yXwKu2z4Qt65qO9JfiLqmOLCerTYHu','jBnipPx1A1ZDPgq9JhvBKIOqofT3ln5HLkh9GNxs8L6mP5KDhN','gbyO7BqNHqXne7W3W8jGqkqp1oQeBhl1foUWnetDBWyUXu2k7F','Ba50oLjfEintviiXEjVZKDdxojQC2rlsvI1CaZ3iELg49K4ImI','1T7sKvP80d5mUemDm6sr0OP9af4bR7ZzWns0DTDaBY41Z2L3lg','JyEusfJr0TL6f88iosL0ljUQkfxycRCmVbHSN5p8RYp0LQaFeP','lnKEC7zbqKJBp9EMJEZOdLrIc6RbYtyE5HpB4tyy3AApsEs9d4','pYpYO93F9JLsMdD2L3yDbi5zq2hON2rqc6G1469kbxEtIPTemW','LobRvkU7Wkxo1MgNb7WbLGW8akeKWB9A14VnLzzzayG8oSD3Sd','JZeh85qSav42CXd4TS4YPgTrGn6Ec5IVCTgMEzMJ5I8OFe9ZcS']

def get_twitter_api(index):

	global APP_KEY_list
	global APP_SECRET_list

	if index >= len(APP_KEY_list):
		print "Need More APP!"

	APP_KEY = APP_KEY_list[index]
	APP_SECRET = APP_SECRET_list[index]

	twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
	ACCESS_TOKEN = twitter.obtain_access_token()

	twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
	
	return twitter

active_user_list = []
user_file = open('active_users.txt','r')
for line in user_file:
		active_user_list.append(get_screen_name(line))
user_file.close()

current_api_index = 0
twitter = get_twitter_api(current_api_index)

name_list = []
user_file = open('user_name_twitter_crossreference.txt','r')
for line in user_file:
	if line.split()[1] == 'Hit':
		name = line.split()[0]
		if name in active_user_list:
			name_list.append(name)
print len(name_list)

hit_name_list = []
path = os.getcwd() + '/tweets/'	
for name in name_list:
	flag = False
	file = open(os.path.join(path, str(name) + '.txt'),'w+')
	try:
		
		tweets = twitter.get_user_timeline(screen_name = name,count = 200)
		for k in range(len(tweets)):
			text = tweets[k]['text'].encode('utf8')
			
			text = text.replace('\n',' ')
			#text = re.sub('[/"¨”´’{}[+^=*$%_`~#|\]]','',text)
			words = text.lower().split()
			if 'putin' in words or 'putin\'s' in words or 'russia' in words or 'russia\'s' in words:
				flag = True
				file.write(text + '\n')
				print name
				print text
				if name not in hit_name_list:
					hit_name_list.append(name)

	except TwythonError as e:
		if e.error_code == 401:
			os.remove(os.path.join(path, str(name) + '.txt'))
			continue
		
		print e
		current_api_index += 1
		twitter = get_twitter_api(current_api_index)
		print('App index: ' + str(current_api_index) +'\n')
	
		try:
		
			tweets = twitter.get_user_timeline(screen_name = name,count = 200)
			for k in range(len(tweets)):
				text = tweets[k]['text'].encode('utf8')
			
				text = text.replace('\n',' ')
				#text = re.sub('[/"¨”´’{}[+^=*$%_`~#|\]]','',text)
				words = text.lower().split()
				if 'putin' in words or 'putin\'s' in words or 'russia' in words or 'russia\'s' in words:
					flag = True
					file.write(text + '\n')
					print name
					print text
					if name not in hit_name_list:
						hit_name_list.append(name)

		except TwythonError as e:
			print e

	if flag == False:
		os.remove(os.path.join(path, str(name) + '.txt'))

print hit_name_list
pickle.dump( hit_name_list, open("hit_name_list.p", "wb")) 
