import networkx as nx
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
 
class GN:
    def __init__(self, G):
        self.G_copy = G.copy()
        self.G = G
        self.partition = [[n for n in G.nodes()]]
        self.all_Q = [0.0]
        self.max_Q = 0.0
        self.zidian={0:[0]}

    
    #Using max_Q to divide communities 
    def run(self):
		#Until there is no edge in the graph
        while len(self.G.edges()) != 0:
			#Find the most betweenness edge
            edge = max(nx.edge_betweenness_centrality(self.G).items(),key=lambda item:item[1])[0]
            
            self.G.remove_edge(edge[0], edge[1])     #一条边的两个点
 
			#List the the connected nodes
            components = [list(c) for c in list(nx.connected_components(self.G))]     #找联通子图
 
            if len(components) != len(self.partition):             #所有的边删掉后每个节点自己是一个联通子图
				#compute the Q
                cur_Q = self.cal_Q(components, self.G_copy)
                if cur_Q not in self.all_Q:
                    self.all_Q.append(cur_Q)
                if cur_Q > self.max_Q:
                    self.max_Q = cur_Q
                    self.partition = components
                    for i in range(len(self.partition)):
                        self.zidian[i]=self.partition[i]
        print('The number of Communites:', len(self.partition))
        print("Communites:", self.partition)
        return self.partition
 
    def cal_Q(self,partition,G):
        m = len(G.edges(None, False))
        a = []
        e = []
        for community in partition:                   #把每一个联通子图拿出来
            t = 0.0
            for node in community:                    #找出联通子图的每一个顶点
                t += len([x for x in G.neighbors(node)])            #G.neighbors(node)找node节点的邻接节点
            a.append(t/(2*m))
#             self.zidian[t/(2*m)]=community
        for community in partition:
            t = 0.0
            for i in range(len(community)):
                for j in range(len(community)):
                    if(G.has_edge(community[i], community[j])):
                        t += 1.0
            e.append(t/(2*m))
        
        q = 0.0
        for ei,ai in zip(e,a):
            q += (ei - ai**2) 
        return q 
    
    def add_group(self):
        num = 0
        nodegroup = {}
        for partition in self.partition:
            for node in partition:
                nodegroup[node] = {'group':num}
            num = num + 1  
        nx.set_node_attributes(self.G_copy, nodegroup)        #给每个节点增加分组的属性值
        #print(nodegroup)
        
    def to_gml(self):
        nx.write_gml(self.G_copy, 'outtoGN.gml')
 
 
def setColor():
    color_map=[]
    color=['red','green','yellow','pink','blue']
    for i in algorithm.G_copy.nodes.data():
        color_map.append(color[i[1]["group"]])
    return color_map
 
if __name__ == '__main__':
    G=nx.read_gml('karate.gml',label='id') #Using max_Q to divide communities 
    algorithm = GN(G)
    algorithm.run()
    algorithm.add_group()
    algorithm.to_gml()
    #print(algorithm.G_copy.nodes.data())       #获取节点数据、属性
    nx.draw(algorithm.G_copy,with_labels=True,node_color=setColor())
    plt.show()