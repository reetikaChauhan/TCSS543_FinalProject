# Network Flow Algorithms - TCSS 543 Final Project

## Project Overview

Ford–Fulkerson is a method for computing the maximum flow from a source s to a sink t in a flow network. The algorithm repeatedly searches for augmenting s–t paths in a residual graph and sends possible flow along them until no more such paths exist.

---

## Software and Testing Environment

### Software Version
- **Python**: 3.12.10
- **Operating System**: MacOS
- **Required Libraries**: Standard library only (no external dependencies)

### Compatibility
- Works on Windows, Linux, and macOS
- Python 3.7 or higher required

---

## How to Run the Preflow-Push Algorithm

### Basic Usage

```bash
cd TCSS543_FinalProject
python Algorithms/FordFulkerson.py <input_file>
```

**Example:**
```bash
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt
```

### Command-Line Options

```
python Algorithms/FordFulkerson/FordFulkerson.py input_file

Arguments:
  input_file            Path to input graph file (required)


```

### Example Commands

```bash
# Run with detailed statistics
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt --stats

# Count all s-t paths
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt --count-paths

# Both statistics and path counting
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt --stats --count-paths

# Quiet mode (for automation/scripting)
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt --quiet
```

## How the Ford Fulkerson Algorithm Works

### Algorithm Overview


### Key Concepts

1. **Residual Graph**: Tracks remaining usable capacity after flow pushes.
2. **Augmenting Path**: A path from s to t with positive remaining capacity.
3. **Bottleneck Capacity**: Minimum capacity on the augmenting path. Determines how much additional flow can be sent.
4. **Forward / Backward Edges**: Used to adjust and undo flow when needed.

### Algorithm Steps

1. **Initialization**:
   - Load graph from .txt file as adjacency dict
   - Initialize residual graph where:
    residual[u][v] = capacity
    residual[v][u] = 0
   - flow begins at 0

2. **Main Loop** (while augmentedPath returns flow >0):
   - The augmented Path searches for any Path from s-> t where all edges have positive remaining capacity
   It return
   - **Path**: the list of edges forming the augmenting path
   - **Flow**:  the bottleneck capacity of the path (min capacity on that path)
   - **Update Residual Graph**: forward capacity decreases,backward capacity increases. Which enables future augmenting paths to reroute or undo incorrect pushes.

3. **Termination**:
   - Algorithm terminates when augmentedPath returns flow == 0
   - MMeaning: no s–t path remains → flow is maximum.

### Complexity

- **Time Complexity**: O(E × F) worst case
- **Space Complexity**: O(V + E)

Because we store
  - original graph
  - residual graph
  - visited nodes
  - augmenting path stack
---

## Code Structure

### Directory Organization

```
TCSS543_FinalProject/
│
├── Algorithms/FordFulkerson
│   └──FordFulkerson.py          # Main algorithm implementation
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

```

---

## Routine Descriptions

### `Algorithms/PreflowPush.py`

#### Main Functions

**`Graphinjest.py`**
- Reads input .txt
- Parses edges & capacities
- Builds adjacency dictionary
- Counts vertices & edges

**`fordFulkerson(graph)`**
fordFulkerson() is the main control function that repeatedly invokes augmentedPath() to locate augmenting paths and push flow through the graph. With each iteration it updates the residual graph and accumulates total flow. The function terminates when no further augmenting paths exist and returns the computed maximum flow value.

**`augmentedPath()`**
searches the residual graph for a valid s–t path with available capacity. It returns both the discovered path and its bottleneck capacity. If no such path exists, it returns a flow of zero, indicating termination of the flow process.


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


## Example Output

### Standard Output
```

Computing maximum flow from 's' to 't' using FordFulkerson...

Computing memory usage...

Computing Number of s-t paths...

==================================================
Maximum Flow: 150
Number of augmented s-t paths: 63
Time: 0.010332 seconds
Nodes: 32
Edges: 230
Peak Memory: 33.34 KB
Current Memory: 19.56 KB
==================================================
```

---

## References

- **Textbook**: Algorithm Design by Kleinberg and Tardos
  - Chapter 7.1: Ford-Fulkerson Algorithm
  - Chapter 7.3: Scaling Ford-Fulkerson Algorithm
  - Chapter 7.4: Preflow-Push Algorithm

---
