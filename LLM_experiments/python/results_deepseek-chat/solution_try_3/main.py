"""Main entry point for sequence alignment."""

from pathlib import Path
import json
from alignment.io import load_organisms, save_scores_to_json
from alignment.scoring import load_blosum_matrix
from alignment.nw_align import needleman_wunsch
from phylogeny.tree import build_phylogenetic_tree
from phylogeny.newick import save_newick_files
from phylogeny.visualization import plot_dendrogram
from phylogeny.clustering import get_clusters_at_threshold, load_thresholds
from typing import Dict, Tuple

def calculate_pairwise_scores(
    organisms: Dict[str, str],
    blosum: Dict[str, int]
) -> Dict[Tuple[str, str], int]:
    """Calculate pairwise alignment scores for all organisms.
    
    Args:
        organisms: Dictionary of species to sequences
        blosum: BLOSUM substitution matrix
        
    Returns:
        Dictionary mapping species pairs to alignment scores
    """
    species = list(organisms.keys())
    scores = {}
    
    for i in range(len(species)):
        for j in range(i, len(species)):
            seq1 = organisms[species[i]]
            seq2 = organisms[species[j]]
            score = needleman_wunsch(seq1, seq2, blosum)
            scores[(species[i], species[j])] = score
            # No need to store symmetric scores as we're saving to file
    
    return scores

def load_scores(file_path: str) -> Dict[Tuple[str, str], int]:
    """Load scores from JSON file and convert to tuple keys."""
    with open(file_path, 'r') as f:
        scores = json.load(f)
    return {tuple(k.split('_')): v for k, v in scores.items()}

def main(blosum_version: str = "50"):
    # Load data and calculate scores (as before)
    organisms = load_organisms("./organisms.json")
    blosum = load_blosum_matrix(f"./blosum{blosum_version}.json")
    scores = calculate_pairwise_scores(organisms, blosum)
    
    # Save scores
    scores_file = f"./organisms_scores_blosum{blosum_version}.json"
    save_scores_to_json(scores, scores_file)
    
    # Build phylogenetic tree
    species = list(organisms.keys())
    tree = build_phylogenetic_tree(species, scores)
    
    # Save both Newick formats
    save_newick_files(tree, blosum_version)
    
    print(f"Saved Newick files:")
    print(f"- Simple: tree_blosum{blosum_version}_newick.nw")
    print(f"- With distances: tree_blosum{blosum_version}_newick_with_distance.nw")
    
    # Generate and save dendrogram
    plot_dendrogram(tree, blosum_version)
    print(f"Saved dendrogram: phylogenetic_tree_blosum{blosum_version}.png")
    
    # Load thresholds
    thresholds_file = "./thresholds.txt"
    if not Path(thresholds_file).exists():
        raise FileNotFoundError(f"Thresholds file not found: {thresholds_file}")
    
    thresholds = load_thresholds(thresholds_file)
    
    # Calculate and save clusters for each threshold
    clusters_data = {}
    for threshold in sorted(thresholds):
        clusters = get_clusters_at_threshold(tree, threshold)
        clusters_data[threshold] = clusters
        
        # Print to console
        print(f"\nClusters at threshold {threshold}:")
        for i, cluster in enumerate(clusters, 1):
            print(f"Cluster {i}: {', '.join(cluster)}")
    
    # Save to JSON
    clusters_file = f"./clusters_for_blosum{blosum_version}.json"
    with open(clusters_file, 'w') as f:
        json.dump(clusters_data, f, indent=4)
    print(f"\nSaved clusters to {clusters_file}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--blosum",
        choices=["50", "62"],
        default="50",
        help="BLOSUM matrix version to use (50 or 62)"
    )
    args = parser.parse_args()
    
    main(blosum_version=args.blosum)