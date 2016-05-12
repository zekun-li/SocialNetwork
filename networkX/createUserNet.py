import networkx as nx
import matplotlib.pyplot as plt
import json
import random
from networkx.drawing.nx_agraph import graphviz_layout # windows setting


with open('data/guardian_comments.json') as data_file:    
    rawInfo = json.load(data_file)
with open('data/cid_aid_table.json') as data_file1:
    lutTable= json.load(data_file1)

G=nx.DiGraph()

ct = 0
for ind in range(0, len(rawInfo)):
    ct += 1
    record = rawInfo[ind]
    authorId = record['author_id']
    G.add_node(authorId) #networkX checks existance automatically
   # print record['comment_id'],authorId, record['reply_comment_id']
    if record['reply_comment_id']:
        toCommentId = record['reply_comment_id']
        if toCommentId in lutTable:
            toUserId = lutTable[toCommentId]
            if G.has_edge(authorId,toUserId):
                G[authorId][toUserId]['weight'] += 1
            else:
                G.add_edge(authorId, toUserId, weight = 1)
       # print G.get_edge_data(authorId,toUserId) #print edge weight
	
# ------------------ remove isolate nodes -----------------

G.remove_nodes_from(nx.isolates(G))


largest_cc = len(max(nx.weakly_connected_component_subgraphs(G), key=len))

print ct
print(len(G.nodes()))
print(len(G.edges()))
print largest_cc



#nx.write_gml(G, "data/userGraph.gml")

'''

# ----------------------------- plot figure -------------------------

plt.figure()
# layout graphs with positions using graphviz neato
pos=graphviz_layout(G,prog="neato")

# color nodes the same in each connected subgraph
C=nx.weakly_connected_component_subgraphs(G)
for g in C:
    c=[random.random()]*nx.number_of_nodes(g) # random color...
    nx.draw(g,
         pos,
       #  node_size=40,
         node_color=c,
         vmin=0.0,
         vmax=1.0,
         with_labels=False,
         width = 1.0
         )

plt.show()

'''