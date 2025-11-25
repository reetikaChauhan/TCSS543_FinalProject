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
    import sys
    import time

    if len(sys.argv) < 2:
        print("Usage: python PreflowPush.py <input_file> [source] [sink]")
        sys.exit(1)

    # Parse command line arguments
    input_file = sys.argv[1]
    source = sys.argv[2] if len(sys.argv) > 2 else 's'
    sink = sys.argv[3] if len(sys.argv) > 3 else 't'

    # Load graph
    print(f"Loading graph from {input_file}...")
    graph = load_graph(input_file)
    print(f"Graph loaded: {len(graph)} vertices")

    # Compute max flow
    print(f"\nComputing maximum flow from '{source}' to '{sink}' using Preflow-Push...")
    start_time = time.time()

    max_flow_value = preflow_push_max_flow(graph, source, sink)

    end_time = time.time()
    elapsed = end_time - start_time

    # Output results
    print(f"\n{'='*50}")
    print(f"Maximum Flow: {max_flow_value}")
    print(f"Time: {elapsed:.6f} seconds")
    print(f"{'='*50}\n")
