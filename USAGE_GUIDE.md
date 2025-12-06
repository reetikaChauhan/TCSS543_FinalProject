# TCSS543_FINALPROJECT  - Complete Usage Guide

## Summary
The project consist of Algorithms folder which has 3 subfolders FordFulkerson, ScalingFordFulkerson and PreflowPush. Each file contains python file for algorithm code, read me file (explain code , input and output and how to run the file) and automatedtest files (to test the algorithm for all newly generated graphs) and this code will output csv files in the respective folders. 

TCSS543_FINALPROJECT/
│
├── Algorithms/
│ ├── Graphinjest.py # Loads graphs from .txt files
│ ├── automated_runscriptscsv.md.  # read me for all automated testingfile(batch run)
│ ├── ResultCompare.py # Used to compare algorithm outputs
│ │
│ ├── FordFulkerson/
│ │ ├── automated_fordfulkerson.py # Batch-run FF on all graphs → CSV
│ │ ├── FordFulkerson.py 
│ │ ├── readme.md
│ │ ├── results_fordfulkerson_generated.csv # output of automated_fordfulkerson.py
│ │
│ ├── PreflowPush/
│ │ ├── automated_preflowpush.py # Batch-run Preflow–Push on all graphs
│ │ ├── PreflowPush.py
│ │ ├── results_preflowpush_generated.csv # output of automated_preflowpush.py
│ │
│ ├── ScalingFordFulkerson/
│ ├── automated_scalingFordFukerson.py # Batch-run Scaling FF on all graphs
│ ├── ScalingFordFulkerson.py
│ ├── readme.md
│ ├── results_scaling_ff_generated.csv #output of automated_scalingFordFukerson.py
│
├── GeneratedGraphs/ #created graphs (input)
│ ├── Random/
│ ├── Mesh/
│ ├── Bipartite/
│ ├── FixedDegree/
│
├── GraphGenerators/ # Code that generates random/mesh graphs
│
├── Random/ # Java example source (optional)
├── Mesh/
├── Bipartite/
├── FixedDegree/
│
├── TCSS543_final_project-v2.pdf # Final report
├── USAGE_GUIDE.md # Top-level user instructions
└── .gitignore



---



### Run Algorithm on a Graph

```bash
cd TCSS543_FinalProject

# Basic usage
python Algorithms/PreflowPush/PreflowPush.py Mesh/smallMesh.txt
python Algorithms/FordFulkerson/FordFulkerson.py Mesh/smallMesh.txt
python Algorithms/ScalingFordFulkerson/ScalingFordFulkerson.py Mesh/smallMesh.txt



