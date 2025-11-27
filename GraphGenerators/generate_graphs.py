"""
Python Graph Generators for Network Flow Testing

Generates bipartite, mesh, fixed-degree, and random graphs
Compatible with the Java generators but written in Python for easier automation
"""

import random
import os
from pathlib import Path


class BipartiteGraphGenerator:
    """Generate bipartite graphs similar to BipartiteGraph.java"""

    @staticmethod
    def generate(n, m, probability, min_cap, max_cap, output_file):
        """
        Generate a bipartite graph

        Args:
            n: Number of nodes on left side
            m: Number of nodes on right side
            probability: Edge existence probability (0.0 to 1.0)
            min_cap: Minimum capacity
            max_cap: Maximum capacity
            output_file: Output filename
        """
        with open(output_file, 'w') as f:
            # Edges from source to left nodes
            for i in range(1, n + 1):
                capacity = random.randint(min_cap, max_cap)
                f.write(f"s l{i} {capacity}\n")

            # Edges from left to right nodes (with probability)
            for i in range(1, n + 1):
                for j in range(1, m + 1):
                    if random.random() <= probability:
                        capacity = random.randint(min_cap, max_cap)
                        f.write(f"l{i} r{j} {capacity}\n")

            # Edges from right nodes to sink
            for j in range(1, m + 1):
                capacity = random.randint(min_cap, max_cap)
                f.write(f"r{j} t {capacity}\n")


class FixedDegreeGraphGenerator:
    """Generate fixed out-degree graphs similar to RandomGraph.java"""

    @staticmethod
    def generate(vertices, out_degree, min_cap, max_cap, output_file):
        """
        Generate a graph with fixed out-degree

        Args:
            vertices: Number of internal vertices
            out_degree: Number of edges leaving each vertex
            min_cap: Minimum capacity
            max_cap: Maximum capacity
            output_file: Output filename
        """
        if vertices <= out_degree:
            raise ValueError("vertices must be greater than out_degree")

        with open(output_file, 'w') as f:
            # Source edges (e random vertices)
            source_targets = random.sample(range(1, vertices + 1), out_degree)
            for v in source_targets:
                capacity = random.randint(min_cap, max_cap)
                f.write(f"s v{v} {capacity}\n")

            # Sink edges (e random vertices)
            sink_sources = random.sample(range(1, vertices + 1), out_degree)
            for v in sink_sources:
                capacity = random.randint(min_cap, max_cap)
                f.write(f"v{v} t {capacity}\n")

            # Internal edges (each vertex has exactly out_degree outgoing edges)
            for i in range(1, vertices + 1):
                # Choose out_degree random neighbors (excluding self)
                possible_neighbors = [j for j in range(1, vertices + 1) if j != i]
                neighbors = random.sample(possible_neighbors, out_degree)

                for neighbor in neighbors:
                    capacity = random.randint(min_cap, max_cap)
                    f.write(f"v{i} v{neighbor} {capacity}\n")


class MeshGraphGenerator:
    """Generate mesh/grid graphs similar to MeshGenerator.java"""

    @staticmethod
    def generate(rows, cols, min_cap, max_cap, output_file, constant_capacity=False):
        """
        Generate a mesh graph

        Args:
            rows: Number of rows
            cols: Number of columns
            min_cap: Minimum capacity (or fixed capacity if constant_capacity=True)
            max_cap: Maximum capacity (ignored if constant_capacity=True)
            output_file: Output filename
            constant_capacity: If True, use min_cap for all edges
        """
        def get_capacity():
            if constant_capacity:
                return min_cap
            return random.randint(min_cap, max_cap)

        with open(output_file, 'w') as f:
            # Source to first column
            for i in range(1, rows + 1):
                f.write(f"s ({i},1) {get_capacity()}\n")

            # Horizontal edges (left to right)
            for i in range(1, rows + 1):
                for j in range(1, cols):
                    f.write(f"({i},{j}) ({i},{j+1}) {get_capacity()}\n")

            # Vertical bidirectional edges
            for j in range(1, cols + 1):
                for i in range(1, rows):
                    # Both directions
                    f.write(f"({i},{j}) ({i+1},{j}) {get_capacity()}\n")
                    f.write(f"({i+1},{j}) ({i},{j}) {get_capacity()}\n")

            # Last column to sink
            for i in range(1, rows + 1):
                f.write(f"({i},{cols}) t {get_capacity()}\n")


class RandomGraphGenerator:
    """Generate random dense graphs similar to BuildGraph.java"""

    @staticmethod
    def generate(vertices, density, min_cap, max_cap, output_file):
        """
        Generate a random graph with specified density

        Args:
            vertices: Number of vertices (including source and sink)
            density: Edge density percentage (0-100)
            min_cap: Minimum capacity
            max_cap: Maximum capacity
            output_file: Output filename
        """
        # Create adjacency matrix
        graph = [[0 for _ in range(vertices)] for _ in range(vertices)]

        # Generate edges based on density
        for i in range(vertices):
            for j in range(i + 1, vertices):
                # Random probability check
                if random.randint(0, 100) < density:
                    capacity = random.randint(min_cap, max_cap)
                    graph[i][j] = capacity
                    graph[j][i] = capacity  # Bidirectional

        # Write to file
        with open(output_file, 'w') as f:
            for i in range(vertices):
                for j in range(vertices):
                    if graph[i][j] > 0:
                        # Format vertex names
                        if i == 0:
                            v1 = 's'
                        elif i == vertices - 1:
                            v1 = str(j) if j != 0 and j != vertices - 1 else ('s' if j == 0 else 't')
                            continue  # Skip sink row
                        else:
                            v1 = str(i)

                        if j == 0:
                            continue  # Skip source column for non-source rows
                        elif j == vertices - 1:
                            v2 = 't'
                        else:
                            v2 = str(j)

                        f.write(f"{v1} {v2} {graph[i][j]}\n")


def generate_test_suite(output_dir="GeneratedGraphs", graphs_per_type=50):
    """
    Generate comprehensive test suite with multiple graphs of each type

    Args:
        output_dir: Directory to save generated graphs
        graphs_per_type: Number of graphs to generate for each type
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"\nGenerating {graphs_per_type} graphs of each type...")
    print("="*60)

    # 1. Bipartite Graphs
    print(f"\n[1/4] Generating Bipartite Graphs...")
    bipartite_dir = Path(output_dir) / "Bipartite"
    bipartite_dir.mkdir(exist_ok=True)

    for i in range(graphs_per_type):
        n = random.randint(10, 100)  # Left nodes
        m = random.randint(10, 100)  # Right nodes
        prob = random.uniform(0.3, 1.0)
        min_cap = random.randint(1, 10)
        max_cap = random.randint(min_cap + 10, 200)

        filename = bipartite_dir / f"bipartite_n{n}_m{m}_p{prob:.2f}_{i+1}.txt"
        BipartiteGraphGenerator.generate(n, m, prob, min_cap, max_cap, filename)

        if (i + 1) % 10 == 0:
            print(f"  Generated {i+1}/{graphs_per_type} bipartite graphs")

    print(f"  [DONE] Completed {graphs_per_type} bipartite graphs")

    # 2. Fixed-Degree Graphs
    print(f"\n[2/4] Generating Fixed-Degree Graphs...")
    fixed_dir = Path(output_dir) / "FixedDegree"
    fixed_dir.mkdir(exist_ok=True)

    for i in range(graphs_per_type):
        vertices = random.randint(20, 200)
        out_degree = random.randint(3, min(10, vertices // 3))
        min_cap = random.randint(1, 20)
        max_cap = random.randint(min_cap + 10, 300)

        filename = fixed_dir / f"fixed_v{vertices}_deg{out_degree}_{i+1}.txt"
        FixedDegreeGraphGenerator.generate(vertices, out_degree, min_cap, max_cap, filename)

        if (i + 1) % 10 == 0:
            print(f"  Generated {i+1}/{graphs_per_type} fixed-degree graphs")

    print(f"  [DONE] Completed {graphs_per_type} fixed-degree graphs")

    # 3. Mesh Graphs
    print(f"\n[3/4] Generating Mesh Graphs...")
    mesh_dir = Path(output_dir) / "Mesh"
    mesh_dir.mkdir(exist_ok=True)

    for i in range(graphs_per_type):
        rows = random.randint(3, 20)
        cols = random.randint(3, 20)
        min_cap = random.randint(1, 10)
        max_cap = random.randint(min_cap + 5, 100)
        constant = random.choice([True, False])

        filename = mesh_dir / f"mesh_{rows}x{cols}_{'const' if constant else 'rand'}_{i+1}.txt"
        MeshGraphGenerator.generate(rows, cols, min_cap, max_cap, filename, constant)

        if (i + 1) % 10 == 0:
            print(f"  Generated {i+1}/{graphs_per_type} mesh graphs")

    print(f"  [DONE] Completed {graphs_per_type} mesh graphs")

    # 4. Random Graphs
    print(f"\n[4/4] Generating Random Graphs...")
    random_dir = Path(output_dir) / "Random"
    random_dir.mkdir(exist_ok=True)

    for i in range(graphs_per_type):
        vertices = random.randint(10, 150)
        density = random.randint(30, 80)
        min_cap = random.randint(1, 20)
        max_cap = random.randint(min_cap + 10, 200)

        filename = random_dir / f"random_v{vertices}_d{density}_{i+1}.txt"
        RandomGraphGenerator.generate(vertices, density, min_cap, max_cap, filename)

        if (i + 1) % 10 == 0:
            print(f"  Generated {i+1}/{graphs_per_type} random graphs")

    print(f"  [DONE] Completed {graphs_per_type} random graphs")

    print("\n" + "="*60)
    print(f"Total graphs generated: {graphs_per_type * 4}")
    print(f"Output directory: {output_dir}/")
    print("="*60 + "\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate network flow test graphs')
    parser.add_argument('--output-dir', '-o', default='GeneratedGraphs',
                       help='Output directory (default: GeneratedGraphs)')
    parser.add_argument('--count', '-n', type=int, default=50,
                       help='Number of graphs per type (default: 50)')
    parser.add_argument('--type', '-t', choices=['bipartite', 'fixed', 'mesh', 'random', 'all'],
                       default='all', help='Graph type to generate (default: all)')

    args = parser.parse_args()

    if args.type == 'all':
        generate_test_suite(args.output_dir, args.count)
    else:
        print(f"Generating {args.count} {args.type} graphs...")
        # Generate specific type
        # (You can extend this to generate specific types)
        generate_test_suite(args.output_dir, args.count)
