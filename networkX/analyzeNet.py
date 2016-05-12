import networkx as nx
import matplotlib.pyplot as plt
import json
import random
import pickle
import sys
from networkx.drawing.nx_agraph import graphviz_layout # windows setting

G = nx.read_gpickle('data/graphFull.gpickle')


 # --------------------- degree-rank plot ------------------------------

degree_sequence=sorted(nx.degree(G).values(),reverse=True) # degree sequence
#print "Degree sequence", degree_sequence
dmax=max(degree_sequence)
#print dmax

plt.figure()
plt.loglog(degree_sequence,'b-',marker='o')
plt.title("Degree rank plot")
plt.ylabel("degree")
plt.xlabel("rank")

# draw graph in inset
plt.axes([0.45,0.45,0.45,0.45])
# layout graphs with positions using graphviz neato
pos=graphviz_layout(G,prog="neato")
# color nodes the same in each connected subgraph
C=nx.weakly_connected_component_subgraphs(G)
for g in C:
    c=[random.random()]*nx.number_of_nodes(g) # random color...
    nx.draw(g,
         pos,
         node_size=20,
         node_color=c,
         vmin=0.0,
         vmax=1.0,
         with_labels=False,
         width = 2.0,
         alpha=0.4
         )


plt.savefig("data/figures/degree_histogram.png")
plt.show()

'''