from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

class CPM():
    
    def __init__(self,G,k=3):
        self._G = G
        self._k = k

    def execute(self):
        # find all cliques which size > k
        cliques = list(nx.find_cliques(G))
        vid_cid = defaultdict(lambda:set())
        for i,c in enumerate(cliques):
            if len(c) < self._k:
                continue
            for v in c:
                vid_cid[v].add(i)
        
        # build clique neighbor
        clique_neighbor = defaultdict(lambda:set())
        remained = set()
        for i,c1 in enumerate(cliques):
            #if i % 100 == 0:
                #print i
            if len(c1) < self._k:
                continue
            remained.add(i)
            s1 = set(c1)
            candidate_neighbors = set()
            for v in c1:
                candidate_neighbors.update(vid_cid[v])
            candidate_neighbors.remove(i)
            for j in candidate_neighbors:
                c2 = cliques[j]
                if len(c2) < self._k:
                    continue
                if j < i:
                    continue
                s2 = set(c2)
                if len(s1 & s2) >= min(len(s1),len(s2)) -1:
                    clique_neighbor[i].add(j)
                    clique_neighbor[j].add(i) 
        
        # depth first search clique neighbors for communities
        communities = []
        for i,c in enumerate(cliques):
            if i in remained and len(c) >= self._k:
                #print 'remained cliques', len(remained)
                communities.append(set(c))
                neighbors = list(clique_neighbor[i])
                while len(neighbors) != 0:
                    n = neighbors.pop()
                    if n in remained:
                        #if len(remained) % 100 == 0:
                            #print 'remained cliques', len(remained)
                        communities[len(communities)-1].update(cliques[n])
                        remained.remove(n)
                        for nn in clique_neighbor[n]:
                            if nn in remained:
                                neighbors.append(nn)
        return communities
        
if __name__ == '__main__':
    # G = nx.karate_club_graph()
    G = nx.read_gml('karate.gml',label='id')
    algorithm = CPM(G, 3)
    communities = algorithm.execute()
    count = 0
    # print(len(G.nodes))
    color_map={}
    for i in range(1,len(G.nodes)):
        color_map[i]='blue'
    # print(color_map)
    node_list = list(G.nodes)
    color=['red','yellow','green','pink','blue']
    for community in communities:
        print(community)
        count += 1
        community = list(community)
        for i in range(len(community)):
            color_map[node_list[community[i]-1]]=color[count-1]
    # color_map=list(color_map)
    color_map1 = [c[1] for c in  sorted(color_map.items(),key=lambda x:x[0])]

    options = {
        "node_color":color_map1,
        "with_labels": True
    }

    nx.draw(G, **options)
    plt.show()