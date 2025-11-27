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
def load_graph(path):
    graph = {}
    edge_count = 0

    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            parts = line.strip().split()
            if len(parts) != 3:
                raise ValueError(
                    f"Error on line {line_num}: '{line.strip()}'\n"
                    f"Expected format: <u> <v> <value>"
                )

            u, v, val = parts[0], parts[1], int(parts[2])
            # Create nodes if not existing
            if u not in graph:
                graph[u] = {}
            if v not in graph:
                graph[v] = {}
            graph[u][v] = val
            edge_count += 1   # count number of input edges

            if u not in graph[v]:
                graph[v][u] = 0

    num_nodes = len(graph)
    return graph, num_nodes, edge_count

def print_graph(graph):
    print("\nGraph Adjacency List\n")
    for u in graph:
        print(f"{u} -> {graph[u]}")
    print("\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: Graphinjest.py <input_file>")
        sys.exit(1)

    path = sys.argv[1]
    graph, nodes, edges = load_graph(path)
    print_graph(graph)
    print("Nodes:", nodes)
    print("Edges:", edges)