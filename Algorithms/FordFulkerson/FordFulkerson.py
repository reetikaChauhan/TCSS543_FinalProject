'''
 Max-Flow(FordFulkerson)
 Initially f(e)=0 for all e in G
 While there is an s-t path in the residual graph Gf
 Let P be a simple s-t path in Gf
 f =augment(f, P)
 Update f to be f'
 Update the residual graph Gf to be Gf'
 Endwhile
 Return f
 '''
'''
augment(f, P)
 Let b=bottleneck(P, f)
 For each edge (u,v)∈P
   If e=(u,v) is a forward edge then
     increase f(e) in G by b
   Else ((u, v) is a backward edge, and let e=(v,u))
     decrease f(e) in G by b
 Endif
 Endfor
 Return(f)
'''


import sys
import tracemalloc
import time
import os
# Add the parent directory (Algorithms) to the module search path so graphinjest loads
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
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
    stpaths =0
    #building residual graph initializing with given graph  with all flow as 0
    for u in graph:
        residualgraph[u] = {}
        for v in graph[u]:
            residualgraph[u][v] = graph[u][v]
    # adding reverse edges       
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
        # counts s-t paths from residual graph
        stpaths += 1 
        
        # print s-t path 
        #path_str = " -> ".join([u for u, v in path] + ["t"])
        #print(f"Path {stpaths}: {path_str} | flow = {flow}")
        # updating residual graph
        for u,v in path:
            residualgraph[u][v] -= flow
            residualgraph[v][u] += flow

    return maxflow,stpaths

input_file = sys.argv[1]
graph, num_nodes, edge_count = load_graph(input_file)
# Compute max flow
print(f"\nComputing maximum flow from 's' to 't' using FordFulkerson...")
tracemalloc.start()          # Start memory tracking
start_time = time.time()
max_flow_value, st_paths = fordFulkerson(graph)
end_time = time.time()
elapsed = end_time - start_time

print(f"\nComputing space complexity...")
current, peak = tracemalloc.get_traced_memory()  # Get memory usage
tracemalloc.stop()           # Stop memory tracking

print(f"\n{'='*50}")
print(f"Maximum Flow: {max_flow_value}")
print(f"Number of s-t paths: {st_paths}")
print(f"Time: {elapsed:.6f} seconds")
print(f"Nodes: {num_nodes}")
print(f"Edges: {edge_count}")
print(f"Peak Memory: {peak / 1024:.2f} KB")
print(f"Current Memory: {current / 1024:.2f} KB")
print(f"{'='*50}\n")






