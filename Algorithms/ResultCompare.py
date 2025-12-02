import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set(style="whitegrid")

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

# Boxplot: Runtime Distribution plot
plt.figure(figsize=(10,6))
sns.boxplot(data=df[["FF_Time", "SFF_Time", "PF_Time"]])
plt.yscale("log")
plt.title("Runtime Distribution (log scale)")
plt.ylabel("Time (seconds, log scale)")
plt.savefig("plot_runtime_boxplot_log.png", dpi=300)
plt.show()

# Mean Runtime per graph type plot
plt.figure(figsize=(10,6))
mean_times = df.groupby("Graph_Type")[["FF_Time","SFF_Time","PF_Time"]].mean()
mean_times.plot(kind="bar", figsize=(10,6), logy=True)
plt.title("Mean Runtime by Graph Type (log scale)")
plt.ylabel("Time (seconds, log scale)")
plt.xticks(rotation=0)
plt.savefig("plot_mean_by_graph_type_log.png", dpi=300)
plt.show()

# Add time per edges 
df["FF_TimePerEdge"] = df["FF_Time"] / df["Edges"]
df["SFF_TimePerEdge"] = df["SFF_Time"] / df["Edges"]
df["PF_TimePerEdge"] = df["PF_Time"] / df["Edges"]

# Runtime per edges plot
plt.figure(figsize=(10,6))
plt.scatter(df["Edges"], df["FF_Time"], label="FF", alpha=0.6)
plt.scatter(df["Edges"], df["SFF_Time"], label="SFF", alpha=0.6)
plt.scatter(df["Edges"], df["PF_Time"], label="PF", alpha=0.6)
plt.title("Runtime vs Number of Edges")
plt.xlabel("Edges")
plt.ylabel("Time (seconds)")
plt.legend()
plt.savefig("plot_time_vs_edges.png", dpi=300)
plt.show()

# Print Average time per edge for different graphs
print("\n=====TIME PER EDGE=====")
print(df.groupby("Graph_Type")[["FF_TimePerEdge","SFF_TimePerEdge","PF_TimePerEdge"]].mean())

# Speedup factors
df["PF_over_FF"] = df["FF_Time"] / df["PF_Time"]
df["PF_over_SFF"] = df["SFF_Time"] / df["PF_Time"]
df["SFF_over_FF"] = df["FF_Time"] / df["SFF_Time"]

print("\n=====SpeedUp Factor=====")
print(df.groupby("Graph_Type")[["PF_over_FF", "PF_over_SFF", "SFF_over_FF"]].mean())

# speedup factors by graphtype plot
plt.figure(figsize=(10,6))
speedup_means = df.groupby("Graph_Type")[["PF_over_FF","PF_over_SFF","SFF_over_FF"]].mean()
speedup_means.plot(kind="bar", figsize=(10,6))
plt.title("Speedup Factors by Graph Type")
plt.ylabel("Speedup Factor (×)")
plt.xticks(rotation=0)
plt.savefig("plot_speedups.png", dpi=300)
plt.show()


print("\n=====COUNT OF WINS (Lower time = winner)=====")

# Overall comparisons
ff_vs_sff = (df["FF_Time"] > df["SFF_Time"]).sum()
sff_vs_ff = (df["SFF_Time"] > df["FF_Time"]).sum()

ff_vs_pf = (df["FF_Time"] > df["PF_Time"]).sum()
pf_vs_ff = (df["PF_Time"] > df["FF_Time"]).sum()

sff_vs_pf = (df["SFF_Time"] > df["PF_Time"]).sum()
pf_vs_sff = (df["PF_Time"] > df["SFF_Time"]).sum()

print(f"Scaling FF beats FF:      {ff_vs_sff} out of {len(df)} graphs")
print(f"FF beats Scaling FF:      {sff_vs_ff} out of {len(df)} graphs\n")

print(f"Preflow beats FF:         {ff_vs_pf} out of {len(df)} graphs")
print(f"FF beats Preflow:         {pf_vs_ff} out of {len(df)} graphs\n")

print(f"Preflow beats Scaling FF: {sff_vs_pf} out of {len(df)} graphs")
print(f"Scaling FF beats Preflow: {pf_vs_sff} out of {len(df)} graphs\n")

# win count bar chart
win_counts = pd.DataFrame({
    "Comparison": ["SFF beats FF","FF beats SFF",
                   "PF beats FF","FF beats PF",
                   "PF beats SFF","SFF beats PF"],
    "Count": [ff_vs_sff, sff_vs_ff, 
              ff_vs_pf, pf_vs_ff,
              sff_vs_pf, pf_vs_sff]
})

plt.figure(figsize=(12,6))
sns.barplot(win_counts, x="Comparison", y="Count")
plt.title("Algorithm Win Counts (Lower Runtime Wins)")
plt.xticks(rotation=45)
plt.savefig("plot_win_counts.png", dpi=300)
plt.show()

# time per edge comparison plot
plt.figure(figsize=(10,6))
tpe = df.groupby("Graph_Type")[["FF_TimePerEdge","SFF_TimePerEdge","PF_TimePerEdge"]].mean()
tpe.plot(kind="bar", figsize=(10,6))
plt.title("Average Time Per Edge by Graph Type")
plt.ylabel("Seconds per Edge")
plt.xticks(rotation=0)
plt.savefig("plot_time_per_edge.png", dpi=300)
plt.show()

# Scatterplot: Augmentations vs Time (FF & SFF Only)
plt.figure(figsize=(10,6))
plt.scatter(df["FF_AugPaths"], df["FF_Time"], label="Ford–Fulkerson", alpha=0.6)
plt.scatter(df["SFF_AugPaths"], df["SFF_Time"], label="Scaling FF", alpha=0.6)
plt.title("Augmenting Paths vs Runtime")
plt.xlabel("Number of Augmentations")
plt.ylabel("Time (seconds)")
plt.legend()
plt.savefig("plot_augmentations_vs_time.png", dpi=300)
plt.show()

# Per-Graph-Type Boxplots
for g in df["Graph_Type"].unique():
    plt.figure(figsize=(8,5))
    subset = df[df["Graph_Type"] == g]
    sns.boxplot(data=subset[["FF_Time", "SFF_Time", "PF_Time"]])
    plt.yscale("log")
    plt.title(f"Runtime Distribution — {g} Graphs (log scale)")
    plt.ylabel("Time (seconds, log scale)")
    plt.savefig(f"plot_{g}_boxplot_log.png", dpi=300)
    plt.show()

# Violin Plots 
plt.figure(figsize=(10,6))
sns.violinplot(data=df[["FF_Time", "SFF_Time", "PF_Time"]], scale="width")
plt.yscale("log")
plt.title("Runtime Distribution (Violin Plot, log scale)")
plt.ylabel("Time (seconds, log scale)")
plt.savefig("plot_runtime_violin_log.png", dpi=300)
plt.show()

# Split the Time-Per-Edge Plot per Graph Type
for alg in ["FF_TimePerEdge", "SFF_TimePerEdge", "PF_TimePerEdge"]:
    plt.figure(figsize=(10,5))
    sns.boxplot(x=df["Graph_Type"], y=df[alg])
    plt.yscale("log")
    plt.title(f"{alg} by Graph Type (log scale)")
    plt.ylabel("Time per Edge (log scale)")
    plt.savefig(f"plot_{alg}_by_type_log.png", dpi=300)
    plt.show()

# WINNER MOSAIC HEATMAP
from matplotlib.colors import ListedColormap

# Step 1: Identify winner for each graph and map to numeric codes
winner_codes = {
    "FF": 0,
    "SFF": 1,
    "PF": 2
}

winner_labels = []

for _, row in df.iterrows():
    if row["SFF_Time"] < row["FF_Time"] and row["SFF_Time"] < row["PF_Time"]:
        winner_labels.append("SFF")
    elif row["PF_Time"] < row["FF_Time"] and row["PF_Time"] < row["SFF_Time"]:
        winner_labels.append("PF")
    else:
        winner_labels.append("FF")

# Reshape into a nice grid (25 rows × 10 columns)
numeric_grid = np.array([winner_codes[w] for w in winner_labels]).reshape(25, 10)

# Step 2: Create discrete colormap: FF=red, SFF=green, PF=blue
cmap = ListedColormap(["red", "green", "blue"])

# Step 3: Plot heatmap mosaic
plt.figure(figsize=(12,6))
sns.heatmap(
    numeric_grid,
    cmap=cmap,
    cbar=False,
    linewidths=0.5,
    linecolor="black"
)

plt.title("Winner Per Graph (FF=Red, SFF=Green, PF=Blue)")
plt.xlabel("Graph Index (Columns)")
plt.ylabel("Graph Index (Rows)")

plt.savefig("plot_winner_mosaic.png", dpi=300)
plt.show()

# ============================
# DONUT CHART OF WINS
# ============================

# Determine winner for each graph
winners = []
for _, row in df.iterrows():
    if row["SFF_Time"] < row["FF_Time"] and row["SFF_Time"] < row["PF_Time"]:
        winners.append("Scaling FF")
    elif row["PF_Time"] < row["FF_Time"] and row["PF_Time"] < row["SFF_Time"]:
        winners.append("Preflow-Push")
    else:
        winners.append("Ford-Fulkerson")

winner_counts = pd.Series(winners).value_counts()

# Donut chart
plt.figure(figsize=(7,7))
colors = ["red", "green", "blue"]  # match heatmap colors

plt.pie(
    winner_counts,
    labels = winner_counts.index,
    autopct="%1.1f%%",
    startangle=90,
    colors=colors,
    wedgeprops={"linewidth": 1, "edgecolor": "white"}
)

# Draw inner circle for donut
centre_circle = plt.Circle((0,0),0.60,fc='white')
plt.gca().add_artist(centre_circle)

plt.title("Overall Algorithm Win Percentage (250 Graphs)")
plt.savefig("plot_donut_winner_distribution.png", dpi=300)
plt.show()
