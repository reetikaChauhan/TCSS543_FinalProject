# Network Flow Algorithms - TCSS 543 Final Project

## Project Overview

This project implements and compares network flow algorithms for maximum flow computation in directed graphs. The implementation focuses on the **Preflow-Push (Push-Relabel) algorithm** with comprehensive testing on various graph types including bipartite, mesh, fixed-degree, and random graphs.

---

## Software and Testing Environment

### Software Version
- **Python**: 3.12.10
- **Operating System**: Windows (tested on Windows 10/11)
- **Required Libraries**: Standard library only (no external dependencies)

### Compatibility
- Works on Windows, Linux, and macOS
- Python 3.7 or higher required

---

## How to Run the Preflow-Push Algorithm

### Basic Usage

```bash
cd TCSS543_FinalProject
python Algorithms/PreflowPush.py <input_file>
```

**Example:**
```bash
python Algorithms/PreflowPush.py Mesh/smallMesh.txt
```

### Command-Line Options

```
python Algorithms/PreflowPush.py [-h] [--source SOURCE] [--sink SINK]
                                  [--stats] [--count-paths]
                                  [--max-paths MAX_PATHS] [--quiet]
                                  input_file

Arguments:
  input_file            Path to input graph file (required)

Optional Arguments:
  -h, --help            Show help message and exit
  --source SOURCE       Source vertex name (default: 's')
  --sink SINK           Sink vertex name (default: 't')
  --stats               Display detailed graph statistics
  --count-paths         Count and display s-t paths
  --max-paths N         Maximum paths to enumerate (default: 1000)
  --quiet, -q           Output only the max flow value
```

### Example Commands

```bash
# Run with detailed statistics
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --stats

# Count all s-t paths
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --count-paths

# Both statistics and path counting
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --stats --count-paths

# Quiet mode (for automation/scripting)
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --quiet
```

## How the Preflow-Push Algorithm Works

### Algorithm Overview

The Preflow-Push algorithm (also known as Push-Relabel) computes maximum flow by maintaining a "preflow" that violates flow conservation at intermediate vertices. It uses a height function to guide flow toward the sink.

### Key Concepts

1. **Preflow**: A flow function that allows vertices (except source and sink) to have excess flow
2. **Height Function**: Assigns a height to each vertex to guide flow downhill toward the sink
3. **Excess**: Amount of incoming flow minus outgoing flow at a vertex
4. **Active Vertex**: A vertex with positive excess (not source or sink)

### Algorithm Steps

1. **Initialization**:
   - Set height of source to n (number of vertices)
   - Saturate all edges leaving the source
   - Initialize excess flow at neighbors of source

2. **Main Loop** (while active vertices exist):
   - Select an active vertex u (has excess flow)
   - **Push**: If possible, push excess from u to a lower neighbor v (where height[u] = height[v] + 1)
   - **Relabel**: If no push is possible, increase height[u] to 1 + minimum height of eligible neighbors

3. **Termination**:
   - Algorithm terminates when no active vertices remain
   - Maximum flow equals the excess at the sink

### Complexity

- **Time Complexity**: O(V²E) worst case
- **Space Complexity**: O(V + E)
  - Graph storage: O(V + E)
  - Flow dictionary: O(E)
  - Excess and height arrays: O(V)

---

## Code Structure

### Directory Organization

```
TCSS543_FinalProject/
│
├── Algorithms/
│   └── PreflowPush.py          # Main algorithm implementation
│
├── GraphGenerators/
│   └── generate_graphs.py      # Python graph generators
│
├── GeneratedGraphs/            # Auto-generated test graphs
│   ├── Bipartite/              # 50 bipartite graphs
│   ├── FixedDegree/            # 50 fixed-degree graphs
│   ├── Mesh/                   # 50 mesh graphs
│   └── Random/                 # 50 random graphs
│
├── Bipartite/                  # Original bipartite test graphs
│   ├── g1.txt                  # Expected max flow: 150
│   └── g2.txt                  # Expected max flow: 898
│
├── FixedDegree/                # Original fixed-degree test graphs
│   ├── 20v-3out-4min-355max.txt    # Expected max flow: 368
│   └── 100v-5out-25min-200max.txt  # Expected max flow: 517
│
├── Mesh/                       # Original mesh test graphs
│   ├── smallMesh.txt           # Expected max flow: 6
│   └── mediumMesh.txt          # Expected max flow: 39
│
├── Random/                     # Original random test graphs
│   ├── n10-m10-cmin5-cmax10-f30.txt    # Expected max flow: 25
│   └── n100-m100-cmin10-cmax20-f949.txt # Expected max flow: 949
│
├── README.md                   # This file
├── USAGE_GUIDE.md             # Detailed usage guide
├── GRAPH_GENERATION_GUIDE.md  # Graph generator documentation
└── test_results.md            # Test results summary
```

---

## Routine Descriptions

### `Algorithms/PreflowPush.py`

#### Main Functions

**`load_graph(path)`**
- Loads a graph from a file in the specified format (from-node, to-node, capacity).
- Returns an adjacency list representation with capacity values.

**`preflow_push_max_flow(graph, source='s', sink='t')`**
- Convenience wrapper function to compute maximum flow using the preflow-push algorithm.
- Returns the maximum flow value from source to sink.

**`count_edges(graph)`**
- Counts the number of edges in the graph that have positive capacity.
- Used for graph statistics and complexity analysis.

**`calculate_space_complexity(graph)`**
- Analyzes and computes the space complexity of the graph representation and algorithm.
- Returns a dictionary with vertex count, edge count, and estimated memory usage.

**`count_st_paths(graph, source, sink, max_paths=None)`**
- Uses DFS to count all simple paths from source to sink.
- Returns the count and list of paths (limited by max_paths to prevent exponential blowup).

**`print_graph_stats(graph, source='s', sink='t', count_paths=False, max_paths=1000)`**
- Prints comprehensive graph statistics including vertices, edges, density, space complexity, and optionally s-t path count.
- Provides formatted output for analysis and reporting.

#### PreflowPush Class

**`PreflowPush.__init__(graph, source, sink)`**
- Initializes the preflow-push algorithm with graph structure and initializes all data structures (flow, excess, height).
- Calls `_initialize_preflow()` to set up initial preflow state.

**`PreflowPush._initialize_preflow()`**
- Sets the source height to n and saturates all edges leaving the source.
- Creates initial excess at source neighbors to start the algorithm.

**`PreflowPush._push(u, v)`**
- Pushes flow from vertex u to vertex v along an edge with residual capacity.
- Updates flow and excess values; only executes when height[u] = height[v] + 1.

**`PreflowPush._relabel(u)`**
- Increases the height of vertex u when no push operation is possible.
- Sets height[u] to 1 + minimum height of neighbors with positive residual capacity.

**`PreflowPush._discharge(u)`**
- Discharges excess flow from vertex u by repeatedly pushing to neighbors or relabeling.
- Continues until vertex u has no excess flow remaining.

**`PreflowPush.max_flow()`**
- Main algorithm driver that processes all active vertices until convergence.
- Returns the maximum flow value (equal to excess at sink).

---

### `GraphGenerators/generate_graphs.py`

#### Generator Classes

**`BipartiteGraphGenerator.generate(n, m, probability, min_cap, max_cap, output_file)`**
- Generates a 3-layer bipartite graph with n left nodes and m right nodes.
- Creates edges based on probability and assigns random capacities in range [min_cap, max_cap].

**`FixedDegreeGraphGenerator.generate(vertices, out_degree, min_cap, max_cap, output_file)`**
- Generates a graph where each vertex has exactly out_degree outgoing edges.
- Ensures uniform structure for testing regular graph performance.

**`MeshGraphGenerator.generate(rows, cols, min_cap, max_cap, output_file, constant_capacity=False)`**
- Generates a 2D mesh/grid graph with bidirectional vertical edges.
- Flow moves horizontally left-to-right and can move vertically up-down.

**`RandomGraphGenerator.generate(vertices, density, min_cap, max_cap, output_file)`**
- Generates a random graph with specified density percentage.
- Creates bidirectional edges with random capacities for general graph testing.

**`generate_test_suite(output_dir="GeneratedGraphs", graphs_per_type=50)`**
- Generates a comprehensive test suite with multiple graphs of each type.
- Creates organized directory structure for systematic testing.

---

## Test Results

All original test cases pass with **100% accuracy**:

| Graph File | Vertices | Edges | Space Complexity | s-t Paths | Expected | Actual | Status |
|------------|----------|-------|------------------|-----------|----------|--------|--------|
| Random/n10-m10-cmin5-cmax10-f30.txt | 11 | 46 | O(11 + 46) | 953 | 25 | 25 | ✓ PASS |
| Random/n100-m100-cmin10-cmax20-f949.txt | 101 | 6,844 | O(101 + 6844) | >10,000 | 949 | 949 | ✓ PASS |
| Mesh/smallMesh.txt | 14 | 31 | O(14 + 31) | 243 | 6 | 6 | ✓ PASS |
| Mesh/mediumMesh.txt | 202 | 570 | O(202 + 570) | >10,000 | 39 | 39 | ✓ PASS |
| Bipartite/g1.txt | 32 | 230 | O(32 + 230) | 200 | 150 | 150 | ✓ PASS |
| Bipartite/g2.txt | 72 | 640 | O(72 + 640) | 570 | 898 | 898 | ✓ PASS |
| FixedDegree/20v-3out-4min-355max.txt | 22 | 66 | O(22 + 66) | >10,000 | 368 | 368 | ✓ PASS |
| FixedDegree/100v-5out-25min-200max.txt | 102 | 510 | O(102 + 510) | >10,000 | 517 | 517 | ✓ PASS |

**Success Rate**: 8/8 (100%)

**Notes:**
- Space Complexity represents total space for graph storage and algorithm overhead: O(V + E)
- s-t Paths shows the number of simple paths from source to sink
- ">10,000" indicates the path count exceeded the enumeration limit (actual count is higher)

---

## Example Output

### Standard Output
```
Loading graph from Mesh/smallMesh.txt...
Graph loaded: 14 vertices, 31 edges

Computing maximum flow from 's' to 't' using Preflow-Push...

============================================================
RESULTS
============================================================
Maximum Flow:          6
Computation Time:      0.001000 seconds
============================================================
```

### With Statistics (--stats)
```
============================================================
GRAPH STATISTICS
============================================================
Vertices (|V|):        14
Edges (|E|):           31
Average degree:        2.21
Density:               0.1703

Source vertex:         s
Sink vertex:           t

------------------------------------------------------------
SPACE COMPLEXITY
------------------------------------------------------------
Graph storage:         O(14 + 31)
Algorithm overhead:    O(14 + 31)
Total space:           O(14 + 31)
Estimated memory:      ~1,440 bytes
                       ~1.41 KB
============================================================
```

### With Path Counting (--count-paths)
```
------------------------------------------------------------
PATH ANALYSIS
------------------------------------------------------------
Counting s-t paths (max 1000)...
Number of s-t paths:   243

First 5 paths from s to t:
  Path 1: s -> (1,1) -> (1,2) -> (1,3) -> (1,4) -> t
  Path 2: s -> (1,1) -> (2,1) -> (2,2) -> (2,3) -> (2,4) -> t
  Path 3: s -> (2,1) -> (2,2) -> (2,3) -> (2,4) -> t
  Path 4: s -> (1,1) -> (1,2) -> (2,2) -> (2,3) -> (2,4) -> t
  Path 5: s -> (1,1) -> (1,2) -> (1,3) -> (2,3) -> (2,4) -> t
  ... and 238 more paths
```

---

## Generating Additional Test Graphs

To create more test graphs for experimentation:

```bash
# Generate 50 graphs of each type
python GraphGenerators/generate_graphs.py --count 50

# Generate 100 graphs of each type
python GraphGenerators/generate_graphs.py --count 100

# Custom output directory
python GraphGenerators/generate_graphs.py --count 25 --output-dir MyGraphs
```

This will create:
- 50 bipartite graphs
- 50 fixed-degree graphs
- 50 mesh graphs
- 50 random graphs

All with randomized parameters for comprehensive testing.

---

## Troubleshooting

### Common Issues

**Problem**: `FileNotFoundError: [Errno 2] No such file or directory`
- **Solution**: Ensure you're in the `TCSS543_FinalProject` directory when running commands

**Problem**: `ModuleNotFoundError: No module named 'X'`
- **Solution**: This implementation uses only Python standard library; ensure Python 3.7+ is installed

**Problem**: Path counting is very slow
- **Solution**: Use `--max-paths 100` to limit path enumeration for dense graphs

**Problem**: Unicode encoding errors on Windows
- **Solution**: Already fixed in current version (uses ASCII characters only)

---

## Performance Notes

- The algorithm runs efficiently on all provided test graphs
- Execution time ranges from <1ms (small graphs) to ~380ms (largest test graph)
- Memory usage is proportional to O(V + E) as expected
- Path counting can be exponential; use `--max-paths` for large dense graphs

---

## References

- **Textbook**: Algorithm Design by Kleinberg and Tardos
  - Chapter 7.1: Ford-Fulkerson Algorithm
  - Chapter 7.3: Scaling Ford-Fulkerson Algorithm
  - Chapter 7.4: Preflow-Push Algorithm

---
