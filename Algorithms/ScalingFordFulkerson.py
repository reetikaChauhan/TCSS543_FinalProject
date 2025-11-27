'''
Scaling Max-Flow
 Initially f(e)=0 for all e in G
 Initially set scaling_parameter to be the largest power of 2 that is no larger
        than the maximum capacity out of s: scaling_param ≤ maxeoutofsce
    While scaling parameter ≥1
        While there is an s-t path in the graph Gf(scaling_parameter)
            Let P be a simple s-t path in Gf(scaling_parameter)
            f =augment(f, P)
            Update f to be f and update Gf(scaling_parameter)
        Endwhile
        scaling_parameter = scaling_parameter/2
 Endwhile
Return f
 '''
import sys
import time
from Graphinjest import load_graph

def augmentedPathWithDelta(residualgraph, s, t, delta):
    stack = [(s, float('inf'), [])]
    visited = set()

    while stack:
        currentnode, flow, path = stack.pop()

        if currentnode == t:
            return path, flow

        visited.add(currentnode)

        for neighbour, capacity in residualgraph[currentnode].items():
            # Only edges with capacity >= delta qualify
            if capacity >= delta and neighbour not in visited:
                flow_min = min(flow, capacity)
                path_new = path + [(currentnode, neighbour)]
                stack.append((neighbour, flow_min, path_new))

    return None, 0


def compute_initial_delta(graph):
    maxcap = max(graph["s"].values())
    delta = 1
    while delta * 2 <= maxcap:
        delta *= 2
    return delta


def scalingFordFulkerson(graph):
    maxflow = 0
    residualgraph = {}

    # Build residual graph
    for u in graph:
        residualgraph[u] = {}
        for v in graph[u]:
            residualgraph[u][v] = graph[u][v]

    # Add reverse edges
    for u in list(residualgraph.keys()):
        for v in list(residualgraph[u].keys()):
            if v not in residualgraph:
                residualgraph[v] = {}
            if u not in residualgraph[v]:
                residualgraph[v][u] = 0

    # Compute initial scaling parameter Δ
    delta = compute_initial_delta(graph)

    # Scaling loop
    while delta >= 1:
        while True:
            path, flow = augmentedPathWithDelta(residualgraph, "s", "t", delta)
            if flow == 0:
                break

            maxflow += flow

            # Update residual graph
            for u, v in path:
                residualgraph[u][v] -= flow
                residualgraph[v][u] += flow

        delta //= 2

    return maxflow


#Main
input_file = sys.argv[1]
graph, num_nodes, edge_count = load_graph(input_file)

print(f"\nComputing max flow with Scaling Max-Flow...")
start = time.time()
max_flow_value = scalingFordFulkerson(graph)
end = time.time()

print(f"\n{'='*50}")
print(f"Maximum Flow: {max_flow_value}")
print(f"Time: {end - start:.6f} seconds")
print(f"Nodes: {num_nodes}")
print(f"Edges: {edge_count}")
print(f"{'='*50}\n")