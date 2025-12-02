# run_all_ff.py
import subprocess
import time

graph_files = [
    "../Bipartite/g2.txt",
    "../Bipartite/g1.txt",
    "../Random/n100-m100-cmin10-cmax20-f949.txt",
    "../Mesh/smallMesh.txt",
    "../Mesh/mediumMesh.txt",
    "../FixedDegree/20v-3out-4min-355max.txt",
    "../FixedDegree/100v-5out-25min-200max.txt",
]

PAUSE_SECONDS = 3  # change this to 1, 2, 3, etc.

def main():
    for path in graph_files:
        print("=" * 80)
        print(f"Running Ford–Fulkerson on: {path}")
        print("=" * 80)

        result = subprocess.run(
            ["python", "FordFulkerson/FordFulkerson.py", path],
            capture_output=True,
            text=True,
        )

        if result.stdout:
            print(">>> STDOUT:")
            print(result.stdout)
        if result.stderr:
            print(">>> STDERR:")
            print(result.stderr)

        print(f"\nPausing {PAUSE_SECONDS} seconds before next run...\n")
        time.sleep(PAUSE_SECONDS)

if __name__ == "__main__":
    main()
