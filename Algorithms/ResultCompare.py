import os
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))

# Read in all CSV results
ff = pd.read_csv(os.path.join(BASE, "FordFulkerson", "results_fordfulkerson_generated.csv"))
sff = pd.read_csv(os.path.join(BASE, "ScalingFordFulkerson", "results_scaling_ff_generated.csv"))
pf = pd.read_csv(os.path.join(BASE, "PreflowPush", "results_preflowpush_generated.csv"))

# Make set up for dataframe that joins all results and keeps number of Aug Paths for FF and SFF
# and distinct times for easier comparison
ff_sel = ff[[
    "Graph_File", "Graph_Type", "Vertices", "Edges", "Space_Complexity", 
    "Actual_Max_Flow", "Augmenting_s-t_Paths", "Computation_Time_Seconds"
]].rename(columns={
    "Augmenting_s-t_Paths": "FF_AugPaths",
    "Computation_Time_Seconds": "FF_Time"
})

sff_sel = sff[[
    "Graph_File", "Augmenting_s-t_Paths", "Computation_Time_Seconds"
]].rename(columns={
    "Augmenting_s-t_Paths": "SFF_AugPaths",
    "Computation_Time_Seconds": "SFF_Time"
})

pf_sel = pf[[
    "Graph_File", "Computation_Time_Seconds"
]].rename(columns={"Computation_Time_Seconds": "PF_Time"})

# Merge to one dataframe
df = (
    ff_sel
    .merge(sff_sel, on="Graph_File")
    .merge(pf_sel, on="Graph_File")
)


# Print analysis of time differences for all graphs and then different types of graphs
print(f"\n===== All GRAPHS =====")
print(df[["FF_Time", "SFF_Time", "PF_Time"]].describe())

graph_types = df["Graph_Type"].unique()

for g in graph_types:
    print(f"\n===== {g} GRAPHS =====")
    subset = df[df["Graph_Type"] == g]
    print(subset[["FF_Time", "SFF_Time", "PF_Time"]].describe())

# Add time per edges 
df["FF_TimePerEdge"] = df["FF_Time"] / df["Edges"]
df["SFF_TimePerEdge"] = df["SFF_Time"] / df["Edges"]
df["PF_TimePerEdge"] = df["PF_Time"] / df["Edges"]

# Print Average time per edge for different graphs
print("\n=====TIME PER EDGE=====")
print(df.groupby("Graph_Type")[["FF_TimePerEdge","SFF_TimePerEdge","PF_TimePerEdge"]].mean())

# Speedup factors
df["PF_over_FF"] = df["FF_Time"] / df["PF_Time"]
df["PF_over_SFF"] = df["SFF_Time"] / df["PF_Time"]
df["SFF_over_FF"] = df["FF_Time"] / df["SFF_Time"]

print("\n=====SpeedUp Factor=====")
print(df.groupby("Graph_Type")[["PF_over_FF", "PF_over_SFF", "SFF_over_FF"]].mean())
