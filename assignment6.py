#안정수, 김대엽
import sys
import datetime
import sys
from math import log
from functools import reduce
import numpy as np

class MinMaxScaler:
    def __init__(self):
        self.max_num = -np.inf
        self.min_num = np.inf

    def fit_transform(self, arr):
        
        self.max_num = np.max(arr)
        self.min_num = np.min(arr)

        return (arr - self.min_num) / (self.max_num - self.min_num)

def graph_entropy(filename):
    
    data = read_file(filename)
    node_w = clac_node_weight(data)
    result = []

    def entropy(c,v):
        deg = 0
        degs = 0
        neighbors = data[v]
        for i in neighbors:
            degs += 1 + node_w[i]
        for i in c & neighbors:
            deg += 1 + node_w[i]
        if degs ==0:
            return 0
        else:
            inner = round(deg / degs,12)
            return 0 if inner == 0 or inner == 1 else \
                -inner*log(inner,2) -(1-inner)*log(1-inner,2)

    candidates = set(data)
    cluster = []
    while candidates:
        v = candidates.pop()
        cluster = data[v].copy()
        cluster.add(v)
        entropies = dict((x,entropy(cluster, x)) for x in data)

        for n in list(cluster): 
            if n == v: continue
            new_c = cluster.copy()
            new_c.remove(n)
            new_e = dict((x,entropy(new_c,x)) for x in data[n])
            if sum(new_e.values()) < sum(entropies[x] for x in data[n]):
                cluster = new_c
                entropies.update(new_e)

        c = reduce(lambda a,b: a | b, (data[x] for x in cluster)) - cluster
        while c:
            n = c.pop()
            new_c = cluster.copy()
            new_c.add(n)
            new_e = dict((x,entropy(new_c,x)) for x in data[n])
            if sum(new_e.values()) < sum(entropies[x] for x in data[n]):
                cluster = new_c
                entropies.update(new_e)
                c &= data[n] - cluster

        candidates -= cluster

        if len(cluster) > 1:
            result.append(cluster)
    return result


def print_label_data(result):
    f = open("project_result.txt", 'w')
    for i in range(len(result)):
        f.write("{}\n".format(str(result[i])[1:-1].replace(',','').replace("'",'') ))
    f.close()
    
    
def read_file(file_name):
    graph = {}
    with open(file_name,'r') as file:
        for line in file:
            f_node,s_node = line.strip().split('\t')
            try:
                graph[f_node].add(s_node)
            except KeyError:
                graph[f_node] = {s_node}
            try:
                graph[s_node].add(f_node)
            except KeyError:
                graph[s_node] = {f_node}
    return graph


def clac_all_node_weight(node_w):
    result = round(sum(x for x in node_w.values()), 4)
    return result


def clac_node_weight(graph):

    nodes = list(graph.keys())
    weight = {k : len(v) for k, v in graph.items()} 
    weights = list(weight.values())
    calc_weights = [x + 1 for x in weights]
    final_weights = [round(1 / x, 4) for x in calc_weights]
    result = dict(zip(nodes, final_weights))
    return result


def clac_edge_weight(file_name,node_w):

    edgesum = []
    edges = []
    edgeweights = []
    anode_w = clac_all_node_weight(node_w)
    nodedict = dict(node_w)
    
    with open(file_name,'r') as file:
        for line in file:
            f_node,s_node = line.strip().split('\t')
            edgesum.append(nodedict[f_node] + nodedict[s_node])
    
    for i in range(len(edgesum)):
        edgeweights.append(round(edgesum[i] / anode_w, 12))
    
    with open(file_name, 'r') as file :
        for line in file:
            edges.append(line.strip().split('\t'))
    
    scaled_edgeweights = MinMaxScaler.fit_transform(edgeweights)
    result = list(zip(edges, scaled_edgeweights))

    return result


if __name__ == "__main__":
    start = datetime.datetime.now()
    cluster = graph_entropy('assignment5_input.txt')
    print_label_data(cluster)
    end = datetime.datetime.now()
    result = (end - start).microseconds
    print(result)