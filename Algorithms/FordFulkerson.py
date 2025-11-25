
def graph_txt(file):
    graph={}
    print("hello there I am working")
    c= 2+3
    print(c)
    with open(file) as f:
        for line in f:
            node1,node2,capacity = line.strip().split()
            capacity = int(capacity)
            if node1 not in graph:
                graph[node1] = {}
            graph[node1][node2] = capacity
            if node2 not in graph:
                graph[node2] ={}

    print(graph)
    return graph

def fordFulkerson(graph):
    maxflow = 0
    residualgraph = {}
    #building residual graph initializing with given graph  with all flow as 0
    for u in graph:
        residualgraph[u] = {}
        for v in graph[u]:
            residualgraph[u][v] = graph[u][v]


graph_txt("Bipartite/output.txt")


