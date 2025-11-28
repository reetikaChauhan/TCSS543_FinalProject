"""
Preflow-Push (Push-Relabel) Algorithm for Maximum Flow

Algorithm Overview:
1. Initialize preflow by pushing maximum flow from source to neighbors
2. Initialize height function (source at height n, others at 0)
3. While there exists an active vertex (with excess flow):
   - If possible, push excess flow to a lower neighbor
   - Otherwise, relabel (increase height) the vertex
4. Return the total flow reaching the sink

Key Data Structures:
- excess[v]: Amount of excess flow at vertex v
- height[v]: Height label of vertex v
- flow[u][v]: Current flow from u to v
"""

from collections import defaultdict, deque
import sys


def load_graph(path):
    """
    Load graph from file in format: <from-node> <to-node> <capacity>
    Returns adjacency list representation with capacities
    """
    graph = {}

    with open(path, "r") as f:
        for line_num, line in enumerate(f, start=1):
            parts = line.strip().split()
            if len(parts) != 3:
                raise ValueError(
                    f"Error on line {line_num}: '{line.strip()}'\n"
                    f"Expected format: <u> <v> <capacity>"
                )

            u, v, capacity = parts[0], parts[1], int(parts[2])

            # Initialize nodes in graph if not present
            if u not in graph:
                graph[u] = {}
            if v not in graph:
                graph[v] = {}

            # Add forward edge with capacity
            graph[u][v] = capacity

            # Add reverse edge with 0 capacity (for residual graph)
            if v not in graph or u not in graph[v]:
                graph[v][u] = 0

    return graph


class PreflowPush:
    """
    Preflow-Push (Push-Relabel) algorithm implementation
    """

    def __init__(self, graph, source, sink):
        """
        Initialize the preflow-push algorithm

        Args:
            graph: Adjacency list with capacities {u: {v: capacity}}
            source: Source vertex
            sink: Sink vertex
        """
        self.graph = graph
        self.source = source
        self.sink = sink

        # Number of vertices
        self.vertices = list(graph.keys())
        self.n = len(self.vertices)

        # Flow on each edge (initially 0)
        self.flow = defaultdict(lambda: defaultdict(int))

        # Excess flow at each vertex
        self.excess = defaultdict(int)

        # Height function for each vertex
        self.height = defaultdict(int)

        # Initialize preflow and heights
        self._initialize_preflow()

    def _initialize_preflow(self):
        """
        Initialize the preflow by:
        1. Setting height of source to n
        2. Saturating all edges from source
        """
        # Set source height to number of vertices
        self.height[self.source] = self.n

        # Saturate all edges leaving the source
        for v in self.graph[self.source]:
            if self.graph[self.source][v] > 0:
                # Send maximum possible flow from source to v
                self.flow[self.source][v] = self.graph[self.source][v]
                self.flow[v][self.source] = -self.graph[self.source][v]

                # Update excess
                self.excess[v] = self.graph[self.source][v]
                self.excess[self.source] -= self.graph[self.source][v]

    def _push(self, u, v):
        """
        Push flow from u to v

        Preconditions:
        - excess[u] > 0
        - residual_capacity(u, v) > 0
        - height[u] = height[v] + 1
        """
        # Calculate residual capacity
        residual = self.graph[u][v] - self.flow[u][v]

        # Push minimum of excess and residual capacity
        delta = min(self.excess[u], residual)

        # Update flows
        self.flow[u][v] += delta
        self.flow[v][u] -= delta

        # Update excesses
        self.excess[u] -= delta
        self.excess[v] += delta

        return delta

    def _relabel(self, u):
        """
        Increase the height of vertex u

        Precondition:
        - excess[u] > 0
        - For all v with residual_capacity(u, v) > 0: height[u] <= height[v]
        """
        # Find minimum height of neighbors with residual capacity
        min_height = float('inf')

        for v in self.graph[u]:
            residual = self.graph[u][v] - self.flow[u][v]
            if residual > 0:
                min_height = min(min_height, self.height[v])

        # Set height to 1 + minimum height of eligible neighbors
        if min_height < float('inf'):
            self.height[u] = min_height + 1

    def _discharge(self, u):
        """
        Discharge excess flow from vertex u by pushing to neighbors
        or relabeling if no push is possible
        """
        while self.excess[u] > 0:
            # Try to push to all neighbors
            pushed = False

            for v in self.graph[u]:
                if self.excess[u] == 0:
                    break

                # Calculate residual capacity
                residual = self.graph[u][v] - self.flow[u][v]

                # Push if possible (residual exists and u is higher than v)
                if residual > 0 and self.height[u] == self.height[v] + 1:
                    self._push(u, v)
                    pushed = True

            # If no push was possible, relabel
            if not pushed and self.excess[u] > 0:
                self._relabel(u)

    def max_flow(self):
        """
        Compute maximum flow from source to sink using preflow-push algorithm

        Returns:
            Maximum flow value
        """
        # Create list of active vertices (vertices with excess, excluding s and t)
        active = deque()

        for v in self.vertices:
            if v != self.source and v != self.sink and self.excess[v] > 0:
                active.append(v)

        # Process active vertices
        while active:
            u = active.popleft()

            # Skip if no longer has excess
            if self.excess[u] == 0:
                continue

            # Discharge excess from u
            old_height = self.height[u]
            self._discharge(u)

            # If height increased, move to front of queue (optimization)
            if self.height[u] > old_height:
                active.appendleft(u)

            # Add neighbors that became active
            for v in self.graph[u]:
                if (v != self.source and v != self.sink and
                    self.excess[v] > 0 and v not in active):
                    active.append(v)

        # Maximum flow is the excess at the sink
        return self.excess[self.sink]


def count_edges(graph):
    """
    Count the number of edges in the graph (only edges with positive capacity)

    Args:
        graph: Adjacency list with capacities

    Returns:
        Number of edges with positive capacity
    """
    edge_count = 0
    for u in graph:
        for v in graph[u]:
            if graph[u][v] > 0:
                edge_count += 1
    return edge_count


def calculate_space_complexity(graph):
    """
    Calculate space complexity of the graph representation

    Returns:
        Dictionary with space complexity breakdown
    """
    num_vertices = len(graph)
    num_edges = count_edges(graph)

    # Space for adjacency list: O(V + E)
    # Each vertex: pointer + data
    # Each edge: neighbor reference + capacity value
    vertex_space = num_vertices * 2  # vertex key + dict object
    edge_space = num_edges * 2       # neighbor key + capacity value

    # Additional space for algorithm:
    # - flow dict: O(E)
    # - excess array: O(V)
    # - height array: O(V)
    algorithm_space = num_edges * 2 + num_vertices * 2

    total_space = vertex_space + edge_space + algorithm_space

    return {
        'vertices': num_vertices,
        'edges': num_edges,
        'graph_space_O': f"O({num_vertices} + {num_edges})",
        'algorithm_space_O': f"O({num_vertices} + {num_edges})",
        'total_space_O': f"O({num_vertices} + {num_edges})",
        'estimated_bytes': total_space * 8  # Assuming 8 bytes per unit
    }


def count_st_paths(graph, source, sink, max_paths=None):
    """
    Count all simple paths from source to sink using DFS

    WARNING: This can be exponential for dense graphs!
    Set max_paths to limit the search.

    Args:
        graph: Adjacency list with capacities
        source: Source vertex
        sink: Sink vertex
        max_paths: Maximum number of paths to find (None = unlimited)

    Returns:
        Tuple of (number_of_paths, list_of_paths or None if max_paths exceeded)
    """
    paths = []
    visited = set()

    def dfs(node, path):
        if max_paths and len(paths) >= max_paths:
            return

        if node == sink:
            paths.append(path[:])
            return

        visited.add(node)

        for neighbor in graph.get(node, {}):
            # Only follow edges with positive capacity
            if graph[node][neighbor] > 0 and neighbor not in visited:
                path.append(neighbor)
                dfs(neighbor, path)
                path.pop()

        visited.remove(node)

    dfs(source, [source])

    return len(paths), paths if not max_paths or len(paths) < max_paths else None


def print_graph_stats(graph, source='s', sink='t', count_paths=False, max_paths=1000):
    """
    Print comprehensive graph statistics

    Args:
        graph: Adjacency list with capacities
        source: Source vertex
        sink: Sink vertex
        count_paths: Whether to count s-t paths
        max_paths: Maximum paths to enumerate
    """
    num_vertices = len(graph)
    num_edges = count_edges(graph)
    space_stats = calculate_space_complexity(graph)

    print("\n" + "="*60)
    print("GRAPH STATISTICS")
    print("="*60)
    print(f"Vertices (|V|):        {num_vertices}")
    print(f"Edges (|E|):           {num_edges}")
    print(f"Average degree:        {num_edges / num_vertices:.2f}")
    print(f"Density:               {num_edges / (num_vertices * (num_vertices - 1)):.4f}")
    print(f"\nSource vertex:         {source}")
    print(f"Sink vertex:           {sink}")

    # Space complexity
    print(f"\n" + "-"*60)
    print("SPACE COMPLEXITY")
    print("-"*60)
    print(f"Graph storage:         {space_stats['graph_space_O']}")
    print(f"Algorithm overhead:    {space_stats['algorithm_space_O']}")
    print(f"Total space:           {space_stats['total_space_O']}")
    print(f"Estimated memory:      ~{space_stats['estimated_bytes']:,} bytes")
    print(f"                       ~{space_stats['estimated_bytes'] / 1024:.2f} KB")

    # Path counting
    if count_paths:
        print(f"\n" + "-"*60)
        print("PATH ANALYSIS")
        print("-"*60)
        print(f"Counting s-t paths (max {max_paths})...")

        num_paths, paths = count_st_paths(graph, source, sink, max_paths)

        print(f"Number of s-t paths:   {num_paths}" +
              (f" (stopped at limit)" if num_paths >= max_paths else ""))

        if paths and num_paths <= 10:
            print(f"\nAll paths from {source} to {sink}:")
            for i, path in enumerate(paths, 1):
                print(f"  Path {i}: {' -> '.join(path)}")
        elif paths:
            print(f"\nFirst 5 paths from {source} to {sink}:")
            for i, path in enumerate(paths[:5], 1):
                print(f"  Path {i}: {' -> '.join(path)}")
            print(f"  ... and {num_paths - 5} more paths")

    print("="*60 + "\n")


def preflow_push_max_flow(graph, source='s', sink='t'):
    """
    Convenience function to compute max flow using preflow-push algorithm

    Args:
        graph: Adjacency list with capacities
        source: Source vertex (default 's')
        sink: Sink vertex (default 't')

    Returns:
        Maximum flow value
    """
    pp = PreflowPush(graph, source, sink)
    return pp.max_flow()


if __name__ == "__main__":
    import time
    import argparse

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Preflow-Push Maximum Flow Algorithm')
    parser.add_argument('input_file', help='Input graph file')
    parser.add_argument('--source', '-s', default='s', help='Source vertex (default: s)')
    parser.add_argument('--sink', '-t', default='t', help='Sink vertex (default: t)')
    parser.add_argument('--stats', action='store_true', help='Show detailed graph statistics')
    parser.add_argument('--count-paths', action='store_true', help='Count s-t paths')
    parser.add_argument('--max-paths', type=int, default=1000,
                       help='Maximum paths to enumerate (default: 1000)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Minimal output (only max flow)')

    args = parser.parse_args()

    # Load graph
    if not args.quiet:
        print(f"Loading graph from {args.input_file}...")
    graph = load_graph(args.input_file)
    if not args.quiet:
        print(f"Graph loaded: {len(graph)} vertices, {count_edges(graph)} edges")

    # Show graph statistics if requested
    if args.stats or args.count_paths:
        print_graph_stats(graph, args.source, args.sink,
                         count_paths=args.count_paths,
                         max_paths=args.max_paths)

    # Compute max flow
    if not args.quiet:
        print(f"Computing maximum flow from '{args.source}' to '{args.sink}' using Preflow-Push...")
    start_time = time.time()

    max_flow_value = preflow_push_max_flow(graph, args.source, args.sink)

    end_time = time.time()
    elapsed = end_time - start_time

    # Output results
    if args.quiet:
        print(max_flow_value)
    else:
        print(f"\n{'='*60}")
        print(f"RESULTS")
        print(f"{'='*60}")
        print(f"Maximum Flow:          {max_flow_value}")
        print(f"Computation Time:      {elapsed:.6f} seconds")
        print(f"{'='*60}\n")
