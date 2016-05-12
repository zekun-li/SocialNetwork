import networkx as nx
import matplotlib.pyplot as plt
import json
import random
import pickle
from networkx.drawing.nx_agraph import graphviz_layout # windows setting


with open('data/guardian_comments.json') as data_file:    
    rawInfo = json.load(data_file)


G=nx.DiGraph()

ct = 0
for ind in range(0, len(rawInfo)/2):
#for ind in range(0, 500):# range(0, 200):
	ct += 1
	record = rawInfo[ind]
	commentId = record['comment_id']
	G.add_node(commentId)
	if record['reply_comment_id']:
		G.add_edge(commentId, record['reply_comment_id'])
	
print ct
print(len(G.nodes()))
print(len(G.edges()))
degdistr=sorted(nx.degree(G).values(), reverse=True)
print(degdistr[:50])

largest_cc = len(max(nx.weakly_connected_component_subgraphs(G), key=len))

print largest_cc

# ------------------ remove isolate nodes and single edges -----------------

G.remove_nodes_from(nx.isolates(G))
'''
def remove_edges(g):
    C = nx.weakly_connected_component_subgraphs(g)
    g2 = nx.DiGraph()
    for c in C:
    	c2 = c.copy()
    	if len(c) == 2:
    		for n in c.nodes():
    			c2.remove_node(n)
    	g2 = nx.disjoint_union(g2,c2)
    return g2
'''
def remove_edges(g): 
    g2 = g.copy()
    C = nx.weakly_connected_component_subgraphs(g)
    for c in C:
    	if len(c) == 2:
    		for n in c.nodes():
    			g2.remove_node(n)
    return g2

G = remove_edges(G)


nx.write_gpickle(G,'data/graphHalf.gpickle')

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
         node_size=40,
         node_color=c,
         vmin=0.0,
         vmax=1.0,
         with_labels=False,
         width = 2.0
         )

#nx.draw(G,pos,node_size = 30)
plt.savefig("data/figures/dnet200.png")

plt.show()


