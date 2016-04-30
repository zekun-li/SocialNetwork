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
from collections import Counter

# ----------------------read user_comment_label.csv to coment_final_label {} -----------------------
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

# -----------------------------------read unigram_bigram_data.npz ----------------------

npzfile = np.load('data/unigram_bigram_data.npz')
X = npzfile['X']
y = npzfile['y']

# ----------------------------------named entity and sentiment -------------------------

def extract_entity_names(t):
    entity_names = []

    if hasattr(t, 'label') and t.label:
        if t.label() == 'NE':
            entity_names.append(' '.join([child[0] for child in t]))
        else:
            for child in t:
                entity_names.extend(extract_entity_names(child))

    return entity_names

comment_entity = []
sentiment_score = []
entity_list = []
pos_name_set = set()
pos_count_list=[]
counter = -1

tokenizer = RegexpTokenizer(r'\w+')
# create English stop words list
en_stop = get_stop_words('en')
# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

for comment in comment_final_label:
	counter += 1
	print counter

	# ---------------- --------------

	text = comment.encode('ascii',errors='ignore')
	text  = re.sub('[/"¨”´’{}[+^=*_`~#|\]]','',text)

	sentences = nltk.sent_tokenize(text)
	tokenized_sentences = [tokenizer.tokenize(sentence) for sentence in sentences]
	# remove stop words from tokens
	stopped_sentences = [[i for i in tokens if not i in en_stop ]for tokens in tokenized_sentences  ]
	# stem token
	stemmed_sentences = [[p_stemmer.stem(i) for i in stopped_tokens] for stopped_tokens in stopped_sentences ]
	# for named-entity
	tagged_sentences = [nltk.pos_tag(sentence) for sentence in stemmed_sentences]
	chunked_sentences = nltk.ne_chunk_sents(tagged_sentences, binary=True)

	# ------------------------------------
	# pos feature
	orig_tag_list = [tag for sentence in tagged_sentences for word,tag in sentence]
	tag_list = [tag.replace('JJR', 'JJ') for tag in orig_tag_list]
	tag_list = [tag.replace('JJS', 'JJ') for tag in tag_list]
	tag_list = [tag.replace('NNS', 'NN') for tag in tag_list]
	tag_list = [tag.replace('NNP', 'NN') for tag in tag_list]
	tag_list = [tag.replace('NNPS', 'NN') for tag in tag_list]
	tag_list = [tag.replace('PRP$', 'PRP') for tag in tag_list]
	tag_list = [tag.replace('RBR', 'RB') for tag in tag_list]
	tag_list = [tag.replace('VBD', 'VB') for tag in tag_list]
	tag_list = [tag.replace('VBG', 'VB') for tag in tag_list]
	tag_list = [tag.replace('VBN', 'VB') for tag in tag_list]
	tag_list = [tag.replace('VBP', 'VB') for tag in tag_list]
	tag_list = [tag.replace('VBZ', 'VB') for tag in tag_list]


	pos_count = Counter(tag_list)
	pos_count_list.append(pos_count)
	pos_name_set = pos_name_set.union(set(tag_list))
	print pos_count
	#print pos_count_list
	print len(pos_count_list)
	print pos_name_set
	print len(pos_name_set)

	# ------------ ---------------
	neg = 0.0
	pos = 0.0
	compound = 0.0
	for sentence in sentences:
		vs = vaderSentiment(sentence)
		#print vs['neg'],vs['pos'],vs['compound']
		neg += vs['neg']
		pos += vs['pos']
		compound += vs['compound']

	# -------------------------------

	#print counter
	entity_names = []
	for tree in chunked_sentences:
	    # Print results per sentence
	    #print tree
	    #print extract_entity_names(tree)
	    extract_entity = extract_entity_names(tree)
	    entity_list.extend(extract_entity)
	    entity_names.extend(extract_entity)

	comment_entity.append(entity_names)
	sentiment_score.append((neg,pos,compound))

entity_list = list(set(entity_list))

nlp_feature = np.zeros((len(comment_final_label),len(entity_list) + 3 )) # named entity + sentiment
pos_feature = np.zeros((len(comment_final_label),len(pos_name_set)))

counter = -1
pos_name_list = list(pos_name_set)
for comment in comment_final_label:
	counter += 1

	for entity in comment_entity[counter]:
			nlp_feature[counter, entity_list.index(entity)] += 1

	nlp_feature[counter,len(entity_list)] = sentiment_score[counter][0]
	nlp_feature[counter,len(entity_list)+ 1] = sentiment_score[counter][1]
	nlp_feature[counter,len(entity_list)+ 2] = sentiment_score[counter][2]

	for pos_name in pos_name_list:
		colIdx = pos_name_list.index(pos_name)
		pos_feature[counter, colIdx] = pos_count_list[counter][pos_name]

#nlp_feature = preprocessing.scale(nlp_feature)
#pos_feature = preprocessing.scale(pos_feature)
X = np.hstack((X,nlp_feature))
X = np.hstack((X,pos_feature))
np.savez('data/unigram_bigram_ner_senti_pos_data.npz',X = X, y = y)

print 'ner cols: '+str(len(entity_list))
print 'senti cols: 3'
print 'pos dimension: ' + str(np.shape(pos_feature))

