#!/usr/bin/env python3
import os
import csv
import time
import sys

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)


from Graphinjest import load_graph
from ScalingFordFulkerson import scalingFordFulkerson


# ---------- PATHS ----------

# Folder where THIS script lives
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root: go up TWO levels: ScalingFordFulkerson -> Algorithms -> TCSS543_FinalProject
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# GeneratedGraphs is directly under the project root
GENERATED_BASE = os.path.join(PROJECT_ROOT, "GeneratedGraphs")

GRAPH_TYPES = {
    "Random":      os.path.join(GENERATED_BASE, "Random"),
    "Mesh":        os.path.join(GENERATED_BASE, "Mesh"),
    "Bipartite":   os.path.join(GENERATED_BASE, "Bipartite"),
    "FixedDegree": os.path.join(GENERATED_BASE, "FixedDegree"),
}

OUTPUT_CSV = os.path.join(SCRIPT_DIR, "results_scaling_ff_generated.csv")


def list_graph_files():
    """
    Collect all .txt graph files under:
      GeneratedGraphs/Random/
      GeneratedGraphs/Mesh/
      GeneratedGraphs/Bipartite/
      GeneratedGraphs/FixedDegree/

    Returns list of (graph_type, full_path, rel_name).
    """
    results = []
    for gtype, folder in GRAPH_TYPES.items():
        folder = os.path.normpath(folder)
        if not os.path.isdir(folder):
            print(f"[WARN] Folder not found for {gtype}: {folder}")
            continue

        for fname in sorted(os.listdir(folder)):
            if not fname.lower().endswith(".txt"):
                continue
            if "read me" in fname.lower():
                continue

            full_path = os.path.join(folder, fname)
            rel_name = f"{gtype}/{fname}"
            results.append((gtype, full_path, rel_name))
    return results


def run_scaling_on_graph(graph, V, E, graph_type, rel_name):
    """
    Run scaling Ford–Fulkerson on a single graph and return stats.
    """
    start = time.time()
    max_flow, num_aug_paths = scalingFordFulkerson(graph)
    end = time.time()
    runtime = end - start

    return {
        "Graph_File": rel_name,
        "Graph_Type": graph_type,
        "Vertices": V,
        "Edges": E,
        "Space_Complexity": f"O({V}+{E})",
        "Augmenting_Paths": num_aug_paths,
        "Max_Flow": max_flow,
        "Time": runtime,
    }


def main():
    print("\n=== Running Scaling Ford–Fulkerson on ALL generated graphs ===\n")

    graph_files = list_graph_files()
    if not graph_files:
        print("No graph files found under GeneratedGraphs/. Check paths.")
        return

    # Open CSV and write header
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Graph_File",
            "Graph_Type",
            "Vertices",
            "Edges",
            "Space_Complexity",
            "Augmenting_s-t_Paths",
            "Actual_Max_Flow",
            "Computation_Time_Seconds",
        ])

        for gtype, full_path, rel_name in graph_files:
            print(f"Processing {rel_name} ...")

            # Load graph (Graphinjest already creates residual-style graph)
            graph, V, E = load_graph(full_path)

            result = run_scaling_on_graph(graph, V, E, gtype, rel_name)

            print(f"  Max Flow         = {result['Max_Flow']}")
            print(f"  Augmenting Paths = {result['Augmenting_Paths']}")
            print(f"  Time (sec)       = {result['Time']:.6f}\n")

            writer.writerow([
                result["Graph_File"],
                result["Graph_Type"],
                result["Vertices"],
                result["Edges"],
                result["Space_Complexity"],
                result["Augmenting_Paths"],
                result["Max_Flow"],
                f"{result['Time']:.6f}",
            ])

    print("\nAll experiments complete.")
    print(f"Results saved to:\n  {OUTPUT_CSV}\n")


if __name__ == "__main__":
    main()
