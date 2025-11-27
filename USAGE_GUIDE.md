# Network Flow Algorithm - Complete Usage Guide

## Summary

You now have a complete implementation of the **Preflow-Push algorithm** with:
- Graph statistics (nodes, edges, space complexity)
- s-t path counting
- 200+ test graphs across 4 graph types
- Python graph generators for creating more test cases

---

## Quick Start

### Run Algorithm on a Graph

```bash
cd TCSS543_FinalProject

# Basic usage
python Algorithms/PreflowPush.py Mesh/smallMesh.txt

# With detailed statistics
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --stats

# With path counting
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --count-paths

# With all features
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --stats --count-paths

# Quiet mode (only max flow value)
python Algorithms/PreflowPush.py Mesh/smallMesh.txt --quiet
```

---

## Command-Line Options

### PreflowPush.py Options

```
usage: PreflowPush.py [-h] [--source SOURCE] [--sink SINK] [--stats]
                      [--count-paths] [--max-paths MAX_PATHS] [--quiet]
                      input_file

positional arguments:
  input_file            Input graph file

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        Source vertex (default: s)
  --sink SINK, -t SINK  Sink vertex (default: t)
  --stats               Show detailed graph statistics
  --count-paths         Count s-t paths
  --max-paths MAX_PATHS Maximum paths to enumerate (default: 1000)
  --quiet, -q           Minimal output (only max flow)
```

### Example Output with --stats

```
============================================================
GRAPH STATISTICS
============================================================
Vertices (|V|):        46
Edges (|E|):           195
Average degree:        4.24
Density:               0.0942

Source vertex:         s
Sink vertex:           t

------------------------------------------------------------
SPACE COMPLEXITY
------------------------------------------------------------
Graph storage:         O(46 + 195)
Algorithm overhead:    O(46 + 195)
Total space:           O(46 + 195)
Estimated memory:      ~7,712 bytes
                       ~7.53 KB
============================================================

RESULTS
============================================================
Maximum Flow:          894
Computation Time:      0.010756 seconds
============================================================
```

### Example Output with --count-paths

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

## Generated Test Graphs

### Available Graphs

You now have **200+ test graphs** in 4 categories:

| Directory | Graph Type | Count | Description |
|-----------|-----------|-------|-------------|
| `GeneratedGraphs/Bipartite/` | Bipartite | 50 | 3-layer matching graphs |
| `GeneratedGraphs/FixedDegree/` | Fixed-Degree | 50 | Regular out-degree graphs |
| `GeneratedGraphs/Mesh/` | Mesh | 50 | 2D grid networks |
| `GeneratedGraphs/Random/` | Random | 50 | Dense random graphs |

Plus original test graphs in:
- `Bipartite/` (g1.txt, g2.txt)
- `FixedDegree/` (20v-3out, 100v-5out)
- `Mesh/` (smallMesh.txt, mediumMesh.txt)
- `Random/` (n10-m10, n100-m100)

### Graph Filename Format

```
Bipartite:    bipartite_n<left>_m<right>_p<prob>_<id>.txt
Fixed-Degree: fixed_v<vertices>_deg<degree>_<id>.txt
Mesh:         mesh_<rows>x<cols>_<const/rand>_<id>.txt
Random:       random_v<vertices>_d<density>_<id>.txt
```

**Examples:**
- `bipartite_n33_m11_p0.42_1.txt` - 33 left, 11 right nodes, 42% edge probability
- `fixed_v127_deg5_1.txt` - 127 vertices, out-degree 5
- `mesh_12x15_rand_1.txt` - 12x15 grid, random capacities
- `random_v94_d67_1.txt` - 94 vertices, 67% density

---

## Generating More Graphs

### Generate Additional Test Graphs

```bash
cd TCSS543_FinalProject

# Generate 50 more graphs of each type
python GraphGenerators/generate_graphs.py --count 50

# Generate 100 graphs of each type
python GraphGenerators/generate_graphs.py --count 100

# Custom output directory
python GraphGenerators/generate_graphs.py --count 25 --output-dir MyGraphs
```

### Generator Parameters

The generator creates graphs with randomized parameters:

**Bipartite:**
- Left nodes: 10-100
- Right nodes: 10-100
- Edge probability: 0.3-1.0
- Capacities: 1-200

**Fixed-Degree:**
- Vertices: 20-200
- Out-degree: 3-10
- Capacities: 1-300

**Mesh:**
- Rows: 3-20
- Columns: 3-20
- Capacities: 1-100
- Mix of constant and random capacity

**Random:**
- Vertices: 10-150
- Density: 30-80%
- Capacities: 1-200

---

## Testing on All Graphs

### Run on All Generated Graphs

```bash
cd TCSS543_FinalProject

# Test on all bipartite graphs
for file in GeneratedGraphs/Bipartite/*.txt; do
    echo "Testing $file"
    python Algorithms/PreflowPush.py "$file" --quiet
done

# Test on all graphs with statistics
for file in GeneratedGraphs/*/*.txt; do
    echo "===== $file ====="
    python Algorithms/PreflowPush.py "$file" --stats
done
```

### Batch Testing Script

Create a file `test_all.sh`:

```bash
#!/bin/bash
for dir in GeneratedGraphs/*/; do
    echo "Testing graphs in $dir"
    for file in "$dir"*.txt; do
        result=$(python Algorithms/PreflowPush.py "$file" --quiet)
        echo "$(basename $file): Max Flow = $result"
    done
done
```

---

## Algorithm Complexity

### Time Complexity
- **Preflow-Push**: O(V²E) worst case
- Efficient for most practical graphs

### Space Complexity
- **Graph Storage**: O(V + E)
- **Algorithm Data Structures**: O(V + E)
  - Flow dictionary: O(E)
  - Excess array: O(V)
  - Height array: O(V)
- **Total**: O(V + E)

---

## Verified Test Cases

All original test cases pass with 100% accuracy:

| Graph File | Vertices | Edges | Expected Flow | Status |
|------------|----------|-------|---------------|--------|
| Random/n10-m10-cmin5-cmax10-f30.txt | 11 | ~30 | 25 | PASS |
| Random/n100-m100-cmin10-cmax20-f949.txt | 101 | ~500 | 949 | PASS |
| Mesh/smallMesh.txt | 14 | 31 | 6 | PASS |
| Mesh/mediumMesh.txt | 202 | ~800 | 39 | PASS |
| Bipartite/g1.txt | 32 | ~200 | 150 | PASS |
| Bipartite/g2.txt | 72 | ~900 | 898 | PASS |
| FixedDegree/20v-3out-4min-355max.txt | 22 | ~60 | 368 | PASS |
| FixedDegree/100v-5out-25min-200max.txt | 102 | ~500 | 517 | PASS |

---

## Next Steps for Your Project

### 1. Implement Other Algorithms

You need to implement two more algorithms for comparison:

- **Ford-Fulkerson** (Chapter 7.1)
  - Basic version using BFS or DFS
  - Find augmenting paths iteratively

- **Scaling Ford-Fulkerson** (Chapter 7.3)
  - Capacity scaling approach
  - Better performance on large capacities

### 2. Create Benchmarking Suite

Compare all three algorithms on various graph types:
- Measure execution time
- Compare number of iterations/operations
- Analyze performance vs. graph properties (size, density, capacity range)

### 3. Empirical Analysis

For your report, analyze:
- Which algorithm is fastest for which graph type?
- How does performance scale with graph size?
- Impact of edge density on performance
- Impact of capacity range on Ford-Fulkerson variants

### 4. Suggested Experiment Structure

```
For each graph type (bipartite, mesh, fixed, random):
  For each size (small, medium, large):
    For each algorithm (FF, Scaling FF, Preflow-Push):
      Run on 10+ graphs
      Measure: time, iterations, memory
      Compute: average, std dev, min, max
```

---

## File Structure

```
TCSS543_FinalProject/
├── Algorithms/
│   └── PreflowPush.py          # Preflow-push implementation
├── GraphGenerators/
│   └── generate_graphs.py      # Python graph generators
├── GeneratedGraphs/
│   ├── Bipartite/              # 50 bipartite graphs
│   ├── FixedDegree/            # 50 fixed-degree graphs
│   ├── Mesh/                   # 50 mesh graphs
│   └── Random/                 # 50 random graphs
├── Bipartite/                  # Original bipartite test graphs
├── FixedDegree/                # Original fixed-degree test graphs
├── Mesh/                       # Original mesh test graphs
├── Random/                     # Original random test graphs
├── GRAPH_GENERATION_GUIDE.md   # How graph generators work
├── USAGE_GUIDE.md              # This file
└── test_results.md             # Test results summary
```

---

## Tips for Your Report

### Methodology Section

Include:
- Description of all three algorithms
- Implementation language (Python)
- Test environment (OS, Python version, hardware)
- Graph generation approach
- Testing methodology

### Results Section

Present:
- Performance comparison tables
- Graphs showing time vs. graph size
- Analysis by graph type
- Statistical significance of results

### Use Your New Tools

```bash
# Get graph statistics for your report
python Algorithms/PreflowPush.py <graph> --stats

# Count paths to understand graph structure
python Algorithms/PreflowPush.py <graph> --count-paths

# Quick benchmarking
time python Algorithms/PreflowPush.py <graph> --quiet
```

---

## Questions or Issues?

Common issues:
1. **Unicode errors**: Fixed (using ASCII arrows)
2. **File not found**: Ensure you're in TCSS543_FinalProject directory
3. **Path counting slow**: Use --max-paths to limit for dense graphs

Good luck with your project!
