import networkx as nx
import json

with open('data/guardian_comments.json') as data_file:    
    rawInfo = json.load(data_file)

myset = set()

cnt = 0 # count the number of reocords
for ind in range(0, len(rawInfo)):
	cnt += 1
	record = rawInfo[ind]
	authorId = record['author_id']
	myset.add(authorId)

print cnt
print len(myset)