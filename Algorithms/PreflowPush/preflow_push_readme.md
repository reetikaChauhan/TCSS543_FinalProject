# Preflow-Push Maximum Flow Algorithm

## Introduction
This project implements the **Preflow-Push (Push-Relabel) Algorithm** to solve the Maximum Flow problem in directed graphs. The goal of this study is to analyze the performance and correctness of the Preflow-Push algorithm across various graph topologies, including Bipartite, Mesh, Fixed-Degree, and Random graphs. Unlike augmenting path algorithms (like Ford-Fulkerson), Preflow-Push relaxes the flow conservation constraint during execution, maintaining a "preflow" and using a height function to push excess flow locally toward the sink.

The results demonstrate that the Preflow-Push implementation is robust and efficient, solving maximum flow problems on graphs with hundreds of vertices and edges in fractions of a second.

## Compilation and Execution
The code is written in **Python 3** and requires no compilation. It relies only on the standard library.

### How to Run
Run the script from the command line, providing the input graph file path.

**Basic Command:**
```bash
python Algorithms/PreflowPush.py <input_file_path>
```

**Options:**
- `--stats`: Show detailed graph statistics (density, space complexity).
- `--count-paths`: Count simple paths from source to sink.
- `--quiet`: Output only the max flow value (useful for batch testing).

**Example:**
```bash
python Algorithms/PreflowPush.py GeneratedGraphs/Mesh/mesh_10x10.txt --stats
```

## Code Structure
The implementation is contained in `Algorithms/PreflowPush.py`.

| Routine | Description |
| :--- | :--- |
| `load_graph(path)` | Parses the input file and constructs an adjacency list representation of the graph with capacities. |
| `PreflowPush.__init__` | Initializes the algorithm, setting up the graph, flow, excess, and height data structures. |
| `PreflowPush._initialize_preflow` | Sets the source height to $|V|$ and saturates all edges leaving the source to create initial excess. |
| `PreflowPush._push(u, v)` | Pushes excess flow from vertex $u$ to $v$ if $u$ is higher ($h(u) = h(v) + 1$) and residual capacity exists. |
| `PreflowPush._relabel(u)` | Increases the height of vertex $u$ to $1 + \min(height(neighbors))$ to allow it to push flow forward or backward. |
| `PreflowPush._discharge(u)` | Repeatedly attempts to push flow from an active vertex $u$ or relabels it until its excess is zero. |
| `PreflowPush.max_flow` | The main loop that manages active vertices (those with excess flow) and discharges them until a valid flow is established. |
| `count_edges(graph)` | Helper that counts the number of edges with positive capacity in the graph. |
| `calculate_space_complexity` | Analyzes and returns the memory usage (Big-O and estimated bytes) of the graph and algorithm structures. |
| `count_st_paths` | Performs a DFS to count the number of simple paths from source to sink (used for graph analysis). |
| `print_graph_stats` | Prints a comprehensive summary of the graph's properties and algorithm's space complexity. |

## Methodology

### Implementation
We implemented the **generic Preflow-Push algorithm** using a FIFO queue for active vertex selection (approximating the standard $O(V^3)$ implementation).
- **Graph Representation:** Adjacency list (dictionary of dictionaries) for $O(1)$ edge lookups.
- **Data Structures:** 
  - `excess`: Dictionary mapping vertices to current excess flow.
  - `height`: Dictionary mapping vertices to their height label.
  - `flow`: Nested dictionary tracking flow on each edge.

### Input Generation
Input graphs were generated using a custom `generate_graphs.py` script that creates four types of graphs:
1. **Bipartite:** Random edges between two sets of vertices.
2. **Mesh:** Grid-like structure with horizontal and vertical edges.
3. **Fixed-Degree:** Random graphs where every vertex has a constant out-degree.
4. **Random:** Erdos-Renyi style random graphs with specified density.

**Source ($s$) and Sink ($t$):**
- For **Mesh**, $s$ is the top-left node, $t$ is the bottom-right.
- For others, $s$ and $t$ are typically node '0' and node '$n-1
 (or specifically labeled 's' and 't' in the file format). The algorithm defaults to looking for 's' and 't' labels but can handle integer IDs.

### Testing Strategy
We performed a systematic investigation:
1. **Correctness:** Verified against 8 "ground truth" files (e.g., `Mesh/smallMesh.txt`, `Bipartite/g1.txt`) with known max flow values. All tests passed.
2. **Performance:** Ran the algorithm on **250 generated instances**:
   - 100 Bipartite graphs
   - 50 Fixed-Degree graphs
   - 50 Mesh graphs
   - 50 Random graphs
3. **Metrics:** Recorded computation time, graph size ($|V|, |E|$), and memory usage.

## Results

### Verification Statistics
We first verified the algorithm on a set of reference graphs with known maximum flow values. The table below summarizes their properties and the algorithm's performance.

| Graph | Vertices ($|V|$) | Edges ($|E|$) | Space Complexity | s-t Paths | Time (s) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mesh (Small)** | 14 | 31 | $O(45)$ | 243 | 0.000 |
| **Mesh (Medium)** | 202 | 570 | $O(772)$ | $>10,000$ | 0.041 |
| **Random (Small)** | 11 | 46 | $O(57)$ | 953 | 0.000 |
| **Random (Large)** | 101 | 6,844 | $O(6,945)$ | $>10,000$ | 0.371 |
| **Bipartite (G1)** | 32 | 230 | $O(262)$ | 200 | 0.000 |
| **Bipartite (G2)** | 72 | 640 | $O(712)$ | 570 | 0.055 |
| **Fixed Degree (Small)** | 22 | 66 | $O(88)$ | $>10,000$ | 0.002 |
| **Fixed Degree (Large)** | 102 | 510 | $O(612)$ | $>10,000$ | 0.067 |

*Note: Space complexity is proportional to $|V| + |E|$. The "s-t Paths" column indicates the complexity of the flow network; graphs with $>10,000$ paths are significantly denser or more interconnected.*

### Aggregate Performance (Generated Graphs)
We then analyzed performance across 250 generated instances with varying sizes ($|V| \in [10, 200]$, $|E| \in [20, 7000]$).

| Graph Type | Count | Avg Time (s) | Max Time (s) | Observations |
| :--- | :--- | :--- | :--- | :--- |
| **Mesh** | 50 | 0.038 | 0.39 | Fastest. The grid structure limits the number of possible paths and back-and-forth pushes. |
| **Fixed-Degree** | 50 | 0.077 | 0.43 | Very consistent performance due to uniform edge distribution. |
| **Random** | 50 | 0.170 | 1.14 | Slower due to unpredictable connectivity and potential for cycles requiring many relabels. |
| **Bipartite** | 100 | 0.177 | 1.62 | Similar to Random; dense bipartite graphs can require significant "lift" (relabeling) to push flow back. |

**Sensitivity Analysis:**
- **Vertices ($|V|$):** The algorithm is most sensitive to the number of vertices. The height function operations and discharge loop scale with $V$, making dense graphs with many nodes (like the large Random graph) significantly slower.
- **Edges ($|E|$):** While more edges increase the work per node discharge, the impact is less than adding nodes.
- **Topology:** Mesh graphs were solved significantly faster than Random graphs of comparable size, suggesting that "path length" and structural rigidity help the algorithm converge faster.

## Future Work
If repeating this experiment, we would:
1. **Compare Heuristics:** Implement the **Gap Heuristic** or **Global Relabeling** to see if they significantly reduce runtime on the denser Random/Bipartite graphs.
2. **Scale Up:** Test on graphs with 10,000+ nodes to better observe the asymptotic behavior ($O(V^3)$ vs $O(V^2 E)$).
3. **Visualization:** Create an animation of the "heights" changing during execution to better understand the "push" dynamics.

**Applications:**
We would be interested in applying this implementation to **Image Segmentation** (foreground/background separation), which can be modeled as a min-cut (max-flow) problem on a grid (Mesh) graph.

## Example Output
Output from `Algorithms/PreflowPush.py Mesh/smallMesh.txt --stats`:
```
GRAPH STATISTICS
Vertices (|V|):        14
Edges (|E|):           31
Average degree:        2.21
Density:               0.1703
Source vertex:         s
Sink vertex:           t

SPACE COMPLEXITY
Graph storage:         O(14 + 31)
Algorithm overhead:    O(14 + 31)
Total space:           O(14 + 31)

RESULTS
Maximum Flow:          6
Computation Time:      0.001000 seconds
```
