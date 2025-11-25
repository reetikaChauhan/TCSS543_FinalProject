
from Graphinjest import load_graph;

def augmentedPath(residualgraph,s,t):
    stack = [(s,float('inf'),[])]
    visited = set()
    while stack:
        currentnode, flow, path = stack.pop()
        if currentnode == t:
            return path, flow
        visited.add(currentnode)
        for neighbour,capacity in residualgraph[currentnode].items():
            if capacity>0 and neighbour not in visited:
                flow_min = min(flow,capacity)
                path_new = path + [( currentnode,neighbour)]
                stack.append((neighbour,flow_min,path_new))
    return None,0

def fordFulkerson(graph):
    maxflow = 0
    residualgraph = {}
    #building residual graph initializing with given graph  with all flow as 0
    for u in graph:
        residualgraph[u] = {}
        for v in graph[u]:
            residualgraph[u][v] = graph[u][v]
           
    for u in list(residualgraph.keys()):
        for v in list(residualgraph[u].keys()):
            if v not in residualgraph:
                residualgraph[v] = {}
            if u not in residualgraph[v]:
                residualgraph[v][u] = 0
    while True:
        path,flow = augmentedPath(residualgraph,"s","t")
        if flow ==0:
            break
        maxflow += flow
        # updating residual graph
        for u,v in path:
            residualgraph[u][v] -= flow
            residualgraph[v][u] += flow

    return maxflow

    
graph = load_graph('FixedDegree/100v-5out-25min-200max.txt')
print(fordFulkerson(graph))



