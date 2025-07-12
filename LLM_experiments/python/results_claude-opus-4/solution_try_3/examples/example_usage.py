"""Example usage of the phylogenetic clustering library."""

import json
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent))

from src.sequence_aligner import SequenceAligner
from src.phylogenetic_tree import PhylogeneticTree
from src.dendrogram import DendrogramPlotter
from src.cluster_analyzer import ClusterAnalyzer


def example_step_by_step():
    """Example of using the library step by step."""
    print("=== Step-by-Step Example ===\n")
    
    # Step 1: Alignment
    print("1. Calculating sequence alignments...")
    aligner = SequenceAligner(blosum_type=62)
    aligner.load_data()
    scores = aligner.calculate_all_alignments()
    print(f"   Calculated {len(scores)} pairwise alignments")
    
    # Step 2: Tree building
    print("\n2. Building phylogenetic tree...")
    tree = PhylogeneticTree(scores, blosum_type=62)
    root = tree.build_tree()
    print(f"   Tree built with root at height {root.height}")
    
    # Step 3: Clustering
    print("\n3. Analyzing clusters...")
    analyzer = ClusterAnalyzer(tree)
    
    # Example thresholds
    example_thresholds = [100, 150, 200]
    clusters = analyzer.analyze_clusters(example_thresholds)
    
    for threshold, cluster_list in clusters.items():
        print(f"   Threshold {threshold}: {len(cluster_list)} clusters")


def example_custom_analysis():
    """Example of custom analysis with the library."""
    print("\n=== Custom Analysis Example ===\n")
    
    # Load existing scores
    with open("organisms_scores_blosum62.json", "r") as f:
        scores_dict = json.load(f)
    
    # Convert to tuple format
    scores = {}
    for key, value in scores_dict.items():
        species1, species2 = key.split("_", 1)
        scores[(species1, species2)] = value
    
    # Build tree
    tree = PhylogeneticTree(scores, blosum_type=62)
    tree.build_tree()
    
    # Find optimal threshold
    print("Finding optimal number of clusters...")
    for threshold in range(50, 250, 25):
        clusters = tree.get_clusters_at_threshold(threshold)
        print(f"  Threshold {threshold}: {len(clusters)} clusters")


def main():
    """Run examples."""
    try:
        example_step_by_step()
        # Uncomment to run custom analysis
        # example_custom_analysis()
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Please run create_sample_data.py first to generate test data.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()