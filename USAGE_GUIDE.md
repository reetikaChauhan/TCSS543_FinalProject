# TCSS543_FINALPROJECT  - Complete Usage Guide

## Summary
The project consist of Algorithms folder which has 3 subfolders FordFulkerson, ScalingFordFulkerson and PreflowPush. Each file contains python file for algorithm code, read me file (explain code , input and output and how to run the file) and automatedtest files (to test the algorithm for all newly generated graphs) and this code will output csv files in the respective folders. 


Flow of the project:
- Run GraphGenerators/generate_graphs.py (see graph generation procedure below)
- Run automated_fordfulkerson.py (see automated_runscriptscsv.md in Algorithms File)
- Run automated_preflowpush.py (see automated_runscriptscsv.md in Algorithms File)
- Run automated_scalingFordFukerson.py (see automated_runscriptscsv.md in Algorithms File)
- Run ResultCompare.py (see ResultCompareREADME.md in Algorithms File)
```

TCSS543_FINALPROJECT/
│
├── Algorithms/
│   ├── Graphinjest.py                       # Loads graphs from .txt files
│   ├── automated_runscriptscsv.md           # Read me for all automated batch scripts
│   ├── ResultCompare.py                     # Used to compare algorithm outputs
│   │
│   ├── FordFulkerson/
│   │   ├── automated_fordfulkerson.py       # Batch-run Ford–Fulkerson on all graphs → CSV
│   │   ├── FordFulkerson.py
│   │   ├── readme.md
│   │   ├── results_fordfulkerson_generated.csv    # Output of automated_fordfulkerson.py
│   │
│   ├── PreflowPush/
│   │   ├── automated_preflowpush.py         # Batch-run Preflow–Push on all graphs
│   │   ├── PreflowPush.py
│   │   ├── results_preflowpush_generated.csv      # Output of automated_preflowpush.py
│   │
│   ├── ScalingFordFulkerson/
│       ├── automated_scalingFordFukerson.py      # Batch-run Scaling FF on all graphs
│       ├── ScalingFordFulkerson.py
│       ├── readme.md
│       ├── results_scaling_ff_generated.csv      # Output of automated_scalingFordFukerson.py
│
├── GeneratedGraphs/                          # created graphs (input)
│   ├── Random/
│   ├── Mesh/
│   ├── Bipartite/
│   ├── FixedDegree/
│
├── GraphGenerators/                           # Code that generates random/mesh graphs
│
├── Random/                                   # Java example source (optional)
├── Mesh/
├── Bipartite/
├── FixedDegree/
│
├── TCSS543_final_project-v2.pdf              # Final report
├── USAGE_GUIDE.md                            # Top-level user instructions
└── .gitignore

```

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


### Run Algorithm on a Graph

```bash
cd TCSS543_FinalProject

# Basic usage
python Algorithms/PreflowPush/PreflowPush.py Mesh/smallMesh.txt
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt
python Algorithms/ScalingFordFulkerson/ScalingFordFulkerson.py Mesh/smallMesh.txt



