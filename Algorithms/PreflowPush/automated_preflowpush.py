#!/usr/bin/env python3
import os
import csv
import time

# Import from your PreflowPush implementation
from PreflowPush import load_graph, preflow_push_max_flow, count_edges


# ---------- PATHS ----------

# Folder where THIS script lives, e.g. .../TCSS543_FinalProject/Algorithms/PreflowPush
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Project root: go up TWO levels: PreflowPush -> Algorithms -> TCSS543_FinalProject
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# GeneratedGraphs is directly under the project root
GENERATED_BASE = os.path.join(PROJECT_ROOT, "GeneratedGraphs")

GRAPH_TYPES = {
    "Random":      os.path.join(GENERATED_BASE, "Random"),
    "Mesh":        os.path.join(GENERATED_BASE, "Mesh"),
    "Bipartite":   os.path.join(GENERATED_BASE, "Bipartite"),
    "FixedDegree": os.path.join(GENERATED_BASE, "FixedDegree"),
}

OUTPUT_CSV = os.path.join(SCRIPT_DIR, "results_preflowpush_generated.csv")


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


def run_preflow_on_graph(graph, graph_type, rel_name):
    """
    Run Preflow–Push on a single graph and return a dict of stats.
    """
    V = len(graph)
    E = count_edges(graph)

    start = time.time()
    max_flow = preflow_push_max_flow(graph, source="s", sink="t")
    end = time.time()
    runtime = end - start

    return {
        "Graph_File": rel_name,
        "Graph_Type": graph_type,
        "Vertices": V,
        "Edges": E,
        "Space_Complexity": f"O({V}+{E})",
        "Max_Flow": max_flow,
        "Time": runtime,
    }


def main():
    print("\n=== Running Preflow–Push on ALL generated graphs ===\n")

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
            "Actual_Max_Flow",
            "Computation_Time_Seconds",
        ])

        for gtype, full_path, rel_name in graph_files:
            print(f"Processing {rel_name} ...")

            # Use PreflowPush.load_graph to read file
            graph = load_graph(full_path)

            result = run_preflow_on_graph(graph, gtype, rel_name)

            print(f"  Max Flow   = {result['Max_Flow']}")
            print(f"  Time (sec) = {result['Time']:.6f}\n")

            writer.writerow([
                result["Graph_File"],
                result["Graph_Type"],
                result["Vertices"],
                result["Edges"],
                result["Space_Complexity"],
                result["Max_Flow"],
                f"{result['Time']:.6f}",
            ])

    print("\nAll experiments complete.")
    print(f"Results saved to:\n  {OUTPUT_CSV}\n")


if __name__ == "__main__":
    main()
