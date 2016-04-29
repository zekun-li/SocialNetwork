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
import gensim
from gensim import corpora, models
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

comment_final_label = {}
f = open('data/user_comment_label.csv','rb')
csv_f = csv.reader(f)
next(csv_f)

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

# preprocess 1->2->3
#npzfile = np.load('data/unigram_bigram_ner_senti_pos_data.npz')
# preprocess 1->3
npzfile = np.load('data/unigram_bigram_data.npz')

X = npzfile['X']
y = npzfile['y']


comment_entity = []
sentiment_score = []
entity_list = []
stemmed_tokens_all = []
#counter = -1

tokenizer = RegexpTokenizer(r'\w+')
# create English stop words list
en_stop = get_stop_words('en')
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

for comment in comment_final_label:

	text = comment.encode('ascii',errors='ignore')
	text  = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',text)

	tokens = tokenizer.tokenize(text)	
	# remove stop words from tokens
	stopped_tokens = [i for i in tokens if not i in en_stop]	
	# stem token
	stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
	stemmed_tokens_all.append(stemmed_tokens)

print 'step 1 of 3 finished'

#  --------------------------generate the lda model -------------------------

#for lda topic modeling
dictionary = corpora.Dictionary(stemmed_tokens_all)
#convert dictionary to bagofwords
corpus = [dictionary.doc2bow(token) for token in stemmed_tokens_all]
topicNum = 40
wordNum = 10
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topicNum, id2word = dictionary, passes=12)
#print(ldamodel.print_topics(num_topics=topicNum, num_words=wordNum))
#outfileName = 'lda_result/'+str(counter)+'_ldamodel'
#ldamodel.save(outfileName)
#convert to features
print 'step 2 of 3 finished'
# --------------------------  query -----------------------------------------

lda_feature = np.zeros((len(comment_final_label),topicNum))
index = 0
for comment in comment_final_label:
	text = comment.encode('ascii',errors='ignore')
	text  = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',text)
	query = tokenizer.tokenize(text)
	query = dictionary.doc2bow(query)
	queryRes = ldamodel[query]
	for queryResEle in queryRes:
		topicInd =  queryResEle[0] #topic index
		prob =  queryResEle[1] #probbility for that topic
		lda_feature[index][topicInd] = prob
	# go to entry of next comment
	index += 1

#lda_feature = preprocessing.scale(lda_feature)	

print 'step 3 of 3 finished.'
print 'lda dimension: '+str(np.shape(lda_feature))

# ------------------------save file ---------------------------------------

X = np.hstack((X,lda_feature))
# preprocess 1->2->3
#np.savez('data/unigram_bigram_ner_senti_pos_lda_data.npz',X = X, y = y)
# preprocess 1->3
np.savez('data/unigram_bigram_lda_data.npz',X = X, y = y)

