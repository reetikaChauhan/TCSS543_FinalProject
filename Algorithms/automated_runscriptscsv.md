# Read me for automated_fordfulkerson.py, automated_preflowpush.py, automated_scalingFordFulkerson.py
# Introduction
Batch runner for Ford–Fulkerson, Scaling Ford Fulkerson and Preflow Push max-flow experiments on the graph instances in folder Generated graphs. Each file will run  for particular algorithm and run that algorithm  on all graph instances and generate csv in each algorithm's folder.


# automated_fordfulkerson.py runs  FordFulkerson.py on all graph instances in the Generated graph folder
# automated_preflowpush.py runs on PreflowPush.py on all graph instances in the Generated graph folder
# automated_scalingFordFulkerson.py runs Scaling FordFulkerson on all graph instances in the Generated graph folder

# Purpose
Purpose of Automated Scripts

Each automated script:

- Scans all graph families (Random, Mesh, Bipartite, FixedDegree)

- Loads each graph using Graphinjest.py

- Runs a specific max-flow algorithm

    - automated_fordfulkerson.py → Ford–Fulkerson

    - automated_preflowpush.py → Preflow–Push

    - automated_scalingFordFukerson.py → Scaling Ford–Fulkerson

- Records performance metrics:

    - Number of vertices

    - Number of edges

    - Space complexity 𝑂(𝑉+𝐸)

    - Max-flow value

    - Number of augmenting paths (if applicable)

    - Runtime

- Saves a CSV report inside the same algorithm folder.

These scripts allow  to automatically produce large-scale experimental data for comparison for TCSS 543 final report.

# How to Run Each Automated Script
python Algorithms/FordFulkerson/automated_fordfulkerson.py
python Algorithms/PreflowPush/automated_preflowpush.py
python Algorithms/ScalingFordFulkerson/automated_scalingFordFukerson.py


# Output:
Each script generates a CSV file under there respective folders such as:

- results_fordfulkerson_generated.csv

- results_preflowpush_generated.csv

- results_scaling_ff_generated.csv

These above 3 files will be later used in the ResultCompare.py file.

| Column Name                | Meaning                                  |
| -------------------------- | ---------------------------------------- |
| `Graph_File`               | Relative file path under GeneratedGraphs |
| `Graph_Type`               | Random / Mesh / Bipartite / FixedDegree  |
| `Vertices`                 | Number of nodes V                        |
| `Edges`                    | Number of edges E                        |
| `Space_Complexity`         | Stored as O(V+E)                         |
| `Augmenting_s-t_Paths`     | Only for FF / Scaling FF                 |
| `Actual_Max_Flow`          | Computed max flow                        |
| `Computation_Time_Seconds` | Wall-clock time                          |


