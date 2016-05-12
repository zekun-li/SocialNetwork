import networkx as nx
import json

with open('data/guardian_comments.json') as data_file:    
    rawInfo = json.load(data_file)

mydict = {}

cnt = 0 # count the number of reocords
for ind in range(0, len(rawInfo)):
	cnt += 1
	record = rawInfo[ind]
	commentId = record['comment_id']
	authorId = record['author_id']
	mydict[commentId] = authorId

with open('data/cid_aid_table.json', 'w') as fp:
    json.dump(mydict, fp)

print cnt
print len(mydict)

