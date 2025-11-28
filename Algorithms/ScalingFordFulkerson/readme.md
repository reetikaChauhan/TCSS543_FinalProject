# Scaling Ford–Fulkerson Algorithm

## Overview

This part of the project implements **Scaling Ford-Fulkerson algorithm** for computing the maximum s–t flow in a directed graph.

Scaling Ford–Fulkerson is an optimization of the classic Ford–Fulkerson method. Instead of exploring all augmenting paths immediately, the algorithm introduces a scaling parameter Δ so that the flow is pushed along large-capacity paths first.

Ultimately leading to fewer iterations and better performance on graphs with large and varied capacities.

---

## Software Development Environment

### Software Version
- **Python**: 3.13.9
- **Operating System**: Windows 11
- **Required Libraries**: Standard library only (no external dependencies)

### Compatibility
- Works on Windows, Linux, and macOS
- Python 3.7 or higher required

---
## How to Run the Preflow-Push Algorithm

### Basic Usage

```bash
cd TCSS543_FinalProject
python Algorithms/ScalingFordFulkerson/ScalingFordFulkerson.py <input_file>
```

**Example/Results:**
```bash
python Algorithms/ScalingFordFulkerson/ScalingFordFulkerson.py /FixedDegree/100v-5out-25min-200max.txt"
```

Computing max flow with Scaling Max-Flow...
```==================================================
Maximum Flow: 517
Time: 0.013279 seconds
Peak Memory: 130.50 KB
Current Memory: 42.72 KB
Nodes: 102
Edges: 510
\# of Augmentations: 16
==================================================
```