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
import tracemalloc
import os
# Add the parent directory (Algorithms) to the module search path so graphinjest loads
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)
from Graphinjest import load_graph

def augmentedPathWithDelta(residualgraph, s, t, delta):
    '''Augment algorithm - 
    Depth-first search (DFS) that finds an s→t augmenting path
    restricted to edges with residual capacity >= delta.

    Each stack entry contains:
        (current_node, bottleneck_so_far, path_edges)

    Returns:
        (path, flow) if an augmenting path is found
        (None, 0)   otherwise
    '''
    # stack for adding neighbors to visit. initialized at starting node
    stack = [(s, float('inf'), [])]
    # set to add visited nodes
    visited = set()

    while stack:

        # pops last entry off stack to explore
        currentnode, flow, path = stack.pop()
        # once we reach sink we return the path and the bottleneck
        if currentnode == t:
            return path, flow
        
        # add current node to visited list
        visited.add(currentnode)

        for neighbour, capacity in residualgraph[currentnode].items():
            # Only edges with capacity >= delta qualify
            if capacity >= delta and neighbour not in visited:
                # takes min of previous flow for current node and the capacity of the edge to neighbor for bottleneck
                # path gets updated with neighbor node
                # new bottleneck and visited path gets put back on the stack
                flow_min = min(flow, capacity)
                path_new = path + [(currentnode, neighbour)]
                stack.append((neighbour, flow_min, path_new))

    return None, 0


def compute_initial_delta(graph):
    '''Computes initial delta for the augmentation selection criteria'''
    maxcap = max(graph["s"].values())
    delta = 1
    while delta * 2 <= maxcap:
        delta *= 2
    return delta


def scalingFordFulkerson(residualgraph):
    '''
    Scaling Max-Flow Algorithm (using an already-built residual graph)

    This function implements the delta-scaling variant of the Ford–Fulkerson method.
    The idea is to restrict augmenting path searches to edges with capacity ≥ delta,
    starting from a large delta and decreasing it gradually. This reduces the number
    of augmentation rounds needed for large graphs with large edge capacities.

    Arguments:
        residualgraph — residual capacity graph:
                        {
                            u : { v : capacity_remaining }
                        }
                        includes both forward and reverse edges. Graph made from Graphinjest.py

    Returns:
        maxflow — the maximum s→t flow value.
    '''
    maxflow = 0
    augpaths =0
    delta = compute_initial_delta(residualgraph)

    while delta >= 1:
        while True:
            # Search for a simple s→t path with every edge having cap ≥ Δ
            path, flow = augmentedPathWithDelta(residualgraph, "s", "t", delta)
            if flow == 0:
                break
            
            # Add bottleneck amount to total max flow
            maxflow += flow
            augpaths += 1
            # Update residual capacities along the found path
            for u, v in path:
                residualgraph[u][v] -= flow
                residualgraph[v][u] += flow

        delta //= 2

    return maxflow, augpaths


#Main
if __name__ == "__main__":
    input_file = sys.argv[1]
    graph, num_nodes, edge_count = load_graph(input_file)

    print(f"\nComputing max flow with Scaling Max-Flow...")
    tracemalloc.start()          # Start memory tracking
    start = time.time()          # Start Time
    max_flow_value, augpaths = scalingFordFulkerson(graph)
    end = time.time()            # End Time
    current, peak = tracemalloc.get_traced_memory()  # Get memory usage
    tracemalloc.stop()           # Stop memory tracking

    print(f"\n{'='*50}")
    print(f"Maximum Flow: {max_flow_value}")
    print(f"Time: {end - start:.6f} seconds")
    print(f"Peak Memory: {peak / 1024:.2f} KB")
    print(f"Current Memory: {current / 1024:.2f} KB")
    print(f"Nodes: {num_nodes}")
    print(f"Edges: {edge_count}")
    print(f"# of Augmentations: {augpaths}")
    print(f"{'='*50}\n")