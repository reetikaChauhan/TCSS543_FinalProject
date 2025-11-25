import sys
import time
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

input_file = sys.argv[1]
graph = load_graph(input_file)
# Compute max flow
print(f"\nComputing maximum flow from 's' to 't' using FordFulkerson...")
start_time = time.time()
max_flow_value = fordFulkerson(graph)
end_time = time.time()
elapsed = end_time - start_time
print(f"\n{'='*50}")
print(f"Maximum Flow: {max_flow_value}")
print(f"Time: {elapsed:.6f} seconds")
print(f"{'='*50}\n")




