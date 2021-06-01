import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.core import _core_subgraph

G = nx.read_gml("karate.gml",label='id')
nx.draw(G, with_labels=True,node_color='y',)
plt.show()

def core_number(G):
    if nx.number_of_selfloops(G) > 0:
        msg = ('Input graph has self loops which is not permitted; '
               'Consider using G.remove_edges_from(nx.selfloop_edges(G)).')
        raise nx.NetworkXError(msg)
    degrees = dict(G.degree())
    # Sort nodes by degree.
    nodes = sorted(degrees, key=degrees.get)
    bin_boundaries = [0]
    curr_degree = 0
    for i, v in enumerate(nodes):
        if degrees[v] > curr_degree:
            bin_boundaries.extend([i] * (degrees[v] - curr_degree))
            curr_degree = degrees[v]
    node_pos = {v: pos for pos, v in enumerate(nodes)}

    core = degrees
    nbrs = {v: list(nx.all_neighbors(G, v)) for v in G}
    for v in nodes:
        for u in nbrs[v]:
            if core[u] > core[v]:
                nbrs[u].remove(v)
                pos = node_pos[u]
                bin_start = bin_boundaries[core[u]]
                node_pos[u] = bin_start
                node_pos[nodes[bin_start]] = pos
                nodes[bin_start], nodes[pos] = nodes[pos], nodes[bin_start]
                bin_boundaries[core[u]] += 1
                core[u] -= 1
    return core
find_cores = core_number
def k_shell(G, k=None, core_number=None):
    def k_filter(v, k, c):
        return c[v] == k
    return _core_subgraph(G, k_filter, k, core_number)

labeldict = {}
for i in range(0,8):
    kc = nx.k_shell(G,k=i)
    for n in kc:
        labeldict[n] = str(i)

options = {
    "labels": labeldict,
    "with_labels": True
}

nx.draw(G, **options)
plt.show()