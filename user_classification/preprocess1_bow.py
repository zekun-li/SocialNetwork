#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import csv
import re
import sys
import numpy as np
from sklearn import preprocessing
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words

comment_final_label = {}
f = open('data/user_comment_label.csv','rb')
csv_f = csv.reader(f)
next(csv_f)

# ------------------------------------- get user-comment dictionary ----------------------

for row in csv_f:
	user_name = row[0].strip() # get user name

	if row[1] or row[1] or row[2]: # if the user has a label
		# aggregate coments
		comment = row[4]
		for ind in range(5,len(row)-1):
			if row[ind] != '':
				comment += ' '
				comment += row[ind]

		# assign label
		if row[1] == '1':
			comment_final_label[comment] = 0 # pro putin
		elif row[2] == '1':
			comment_final_label[comment] = 1 # against putin 
		else:
			comment_final_label[comment] = 2 # can't decide

# ---------------------------------bow unigram --------------------------------

word_dict = {}
for comment in comment_final_label:
	text = comment.encode('ascii',errors='ignore')
	tmp_line = re.sub('[-<>(),.:;!?&]',' ',text)		
	bag_of_words = tmp_line.split()
	for word in bag_of_words:
			word = word.lower()	
			word = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',word)			
			word = word.replace('\'','')		
			if word == '':
				continue		
			if word not in word_dict:
				word_dict[word] = 1
			else:
				word_dict[word] += 1

token_count = 0
vocabulary = {}
for word in word_dict:
	#if word_dict[word]>=5:
	if word_dict[word]>=5:
		vocabulary[word] = token_count
		token_count +=1

print  'unigram dimension: '+str(len(comment_final_label)) +' '+ str(token_count)
X_unigram = np.zeros((len(comment_final_label),token_count))
y = np.zeros(len(comment_final_label))

counter = -1
for comment in comment_final_label:
	counter += 1
	text = comment.encode('ascii',errors='ignore')
	words_dict = {}	
	tmp_line = re.sub('[-<>(),.:;!?&]',' ',text)	
	bag_of_words = tmp_line.split()

	y[counter] = comment_final_label[comment]

	for word in bag_of_words:
		word = word.lower()	
		word = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',word)			
		word = word.replace('\'','')		
		if word == '':
			continue

		if word in vocabulary:
			if word in words_dict:
				words_dict[word] = words_dict[word] + 1		
			else:
				words_dict[word] = 1	

	token_dict = {}
	for word in words_dict:
		token_dict[vocabulary[word]] = words_dict[word]	

	for token in sorted(token_dict):
		X_unigram[counter,token] =  words_dict[word]	


#X_unigram = preprocessing.scale(X_unigram)
#np.savez('data/unigram_data.npz',X = X_unigram, y = y)

# -------------------------------------------bow bi-gram -------------------------------

word_dict ={}
for comment in comment_final_label:
	text = comment.encode('ascii',errors='ignore')
	text  = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',text)
	tmp_line = re.sub('[-<>(),.:;!?&]',' ',text)			
	bag_of_words = tmp_line.split()

	for i in range(len(bag_of_words)):
			word = bag_of_words[i]
			word = word.lower()			
			word = word.replace('\'','')		
			if word == '':
				continue
			
			if i+1 < len(bag_of_words):
				next_word = bag_of_words[i+1]
				next_word = next_word.lower()			
				next_word = next_word.replace('\'','')	
				word = word + '_' + next_word

				if word not in word_dict:
					word_dict[word] = 1
				else:
					word_dict[word] += 1

vocabulary = {}
token_count = 0
for word in word_dict:
	#if word_dict[word]>=8:
	if word_dict[word]>=8:
		vocabulary[word] = token_count
		token_count +=1

X_bigram = np.zeros((len(comment_final_label),token_count))
y = np.zeros(len(comment_final_label))

counter = -1
for comment in comment_final_label:
	counter += 1
	text = comment.encode('ascii',errors='ignore')
	words_dict = {}	
	text  = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',text)
	tmp_line = re.sub('[-<>(),.:;!?&]',' ',text)	
	bag_of_words = tmp_line.split()

	y[counter] = comment_final_label[comment]

	for i in range(len(bag_of_words)):
		word = bag_of_words[i]
		word = word.lower()			
		word = word.replace('\'','')		
		if word == '':
			continue
			
		if i+1 < len(bag_of_words):
			next_word = bag_of_words[i+1]
			next_word = next_word.lower()			
			next_word = next_word.replace('\'','')	
			word = word + '_' + next_word

			if word in vocabulary:
				if word in words_dict:
					words_dict[word] = words_dict[word] + 1		
				else:
					words_dict[word] = 1	

		token_dict = {}
		for word in words_dict:
			token_dict[vocabulary[word]] = words_dict[word]	

		for token in sorted(token_dict):
			X_bigram[counter,token] =  words_dict[word]

print  'bigram dimension: '+str(len(comment_final_label)) +' '+ str(token_count)
#X_bigram = preprocessing.scale(X_bigram)
#np.savez('data/bigram_data.npz',X = X_bigram, y = y)

X = np.hstack((X_unigram,X_bigram))
np.savez('data/unigram_bigram_data.npz',X = X, y = y)
