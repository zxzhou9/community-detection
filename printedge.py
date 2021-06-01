from networkx import *
import sys
import matplotlib.pyplot as plt

G=nx.read_gml('karate.gml',label='id')

# print the adjacency list to a file
try:
    nx.write_edgelist(G, "test.txt", delimiter=' ',data= False )
except TypeError:
    print("Error in writing output to random_graph.txt")

fh = open("test.txt", 'rb')
G = nx.read_adjlist(fh)
fh.close()