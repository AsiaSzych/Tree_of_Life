# main.py

import itertools
import json
import argparse
import os
from pathlib import Path
from typing import Dict, List

from src.utils import load_json_data, load_thresholds
from src.alignment import calculate_nw_score
from src.clustering import (
    build_tree,
    to_newick,
    draw_dendrogram,
    get_clusters_at_threshold
)

def calculate_all_pairs_similarity(
    organisms: Dict[str, str],
    blosum_scores: Dict[str, int]
) -> Dict[str, Dict[str, int]]:
    species_names = list(organisms.keys())
    similarity_matrix = {name: {} for name in species_names}
    for species1, species2 in itertools.combinations(species_names, 2):
        seq1, seq2 = organisms[species1], organisms[species2]
        print(f"Calculating score for: ({species1}, {species2})...")
        score = calculate_nw_score(seq1, seq2, blosum_scores)
        similarity_matrix[species1][species2] = score
        similarity_matrix[species2][species1] = score
    return similarity_matrix

def format_scores_for_saving(
    similarity_matrix: Dict[str, Dict[str, int]],
    species_names: List[str]
) -> Dict[str, int]:
    flat_scores = {}
    for species1, species2 in itertools.combinations(species_names, 2):
        key = f"{species1}_{species2}"
        score = similarity_matrix[species1][species2]
        flat_scores[key] = score
    return flat_scores

def main():
    """
    Main function to run the full phylogenetic analysis pipeline.
    """
    parser = argparse.ArgumentParser(description="Full phylogenetic analysis pipeline.")
    parser.add_argument("organisms_file", type=str, help="Path to organism sequences.")
    parser.add_argument("blosum_file", type=str, help="Path to BLOSUM scores.")
    parser.add_argument("thresholds_file", type=str, help="Path to thresholds file.")
    args = parser.parse_args()

    # --- 1. Load Data ---
    print("--- Loading Data ---")
    organisms = load_json_data(args.organisms_file)
    blosum_scores = load_json_data(args.blosum_file)
    thresholds = load_thresholds(args.thresholds_file)
    species_names = sorted(list(organisms.keys()))
    print("Data loaded successfully.\n")

    # --- 2. Core Analysis ---
    print("--- Calculating Pairwise Similarity Scores ---")
    similarity_matrix = calculate_all_pairs_similarity(organisms, blosum_scores)
    print("\nCalculations complete.\n")

    print("--- Building Phylogenetic Tree ---")
    phylogenetic_tree = build_tree(similarity_matrix, species_names)
    print("Tree constructed successfully.\n")

    # --- 3. Save All Artifacts ---
    print("--- Saving All Output Artifacts ---")
    blosum_filename_stem = Path(args.blosum_file).stem
    blosum_version = ''.join(filter(str.isdigit, blosum_filename_stem))
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    # Save scores
    scores_output_path = os.path.join(output_dir, f"organisms_scores_{blosum_filename_stem}.json")
    flat_scores = format_scores_for_saving(similarity_matrix, species_names)
    with open(scores_output_path, 'w') as f:
        json.dump(flat_scores, f, indent=4)
    print(f"Similarity scores saved to: {scores_output_path}")

    # Save Newick files
    newick_simple_path = os.path.join(output_dir, f"tree{blosum_version}_newick.nw")
    newick_with_dist_path = os.path.join(output_dir, f"tree{blosum_version}_newick_with_distance.nw")
    with open(newick_simple_path, 'w') as f:
        f.write(to_newick(phylogenetic_tree, with_distance=False))
    print(f"Newick tree (no distance) saved to: {newick_simple_path}")
    with open(newick_with_dist_path, 'w') as f:
        f.write(to_newick(phylogenetic_tree, with_distance=True))
    print(f"Newick tree (with distance) saved to: {newick_with_dist_path}")

    # Save Dendrogram
    dendrogram_path = os.path.join(output_dir, f"phylogenetic_tree_blosum{blosum_version}.png")
    draw_dendrogram(phylogenetic_tree, dendrogram_path)
    print(f"Dendrogram saved to: {dendrogram_path}\n")

    # --- 4. Calculate and Save Clusters ---
    print("--- Calculating Clusters for Each Threshold ---")
    all_clusters_results = {}
    for threshold in thresholds:
        clusters = get_clusters_at_threshold(phylogenetic_tree, threshold)
        all_clusters_results[str(threshold)] = clusters

    print("\n--- Final Clustering Results ---")
    print(json.dumps(all_clusters_results, indent=4))

    clusters_output_path = os.path.join(output_dir, f"clusters_for_blosum{blosum_version}.json")
    with open(clusters_output_path, 'w') as f:
        json.dump(all_clusters_results, f, indent=4)
    print(f"\nClustering results saved to: {clusters_output_path}")

if __name__ == "__main__":
    main()