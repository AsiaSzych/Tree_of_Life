import os
import json
from typing import Dict, List

from needleman_wunsch import load_sequences, load_blosum, needleman_wunsch
from tree import (
    build_phylogenetic_tree,
    TreeNode,
    to_newick,
    to_newick_with_distances,
    get_clusters_below_threshold,
)
from dendrogram import draw_dendrogram


def compute_all_pairwise_scores(
    sequences: Dict[str, str], blosum: Dict[str, int]
) -> Dict[str, Dict[str, int]]:
    from itertools import combinations_with_replacement

    species = list(sequences.keys())
    scores = {sp1: {} for sp1 in species}

    for sp1, sp2 in combinations_with_replacement(species, 2):
        seq1 = sequences[sp1]
        seq2 = sequences[sp2]
        score = needleman_wunsch(seq1, seq2, blosum)
        scores[sp1][sp2] = score
        scores[sp2][sp1] = score  # Symmetric

    return scores


def flatten_scores(scores: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    flat_scores = {}
    processed = set()
    for sp1 in scores:
        for sp2 in scores[sp1]:
            pair = tuple(sorted([sp1, sp2]))
            if pair in processed:
                continue
            key = f"{pair[0]}_{pair[1]}"
            flat_scores[key] = int(scores[sp1][sp2])
            processed.add(pair)
    return flat_scores


def save_scores_to_json(scores: Dict[str, int], blosum_filename: str):
    blosum_base = os.path.splitext(os.path.basename(blosum_filename))[0]
    if blosum_base.startswith("blosum"):
        suffix = blosum_base[6:]
    else:
        suffix = blosum_base
    output_filename = f"organisms_scores_blosum{suffix}.json"
    output_path = os.path.join(output_filename)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)
    print(f"Scores saved to {output_path}")


def save_newick_files(tree_root: TreeNode, blosum_filename: str):
    blosum_base = os.path.splitext(os.path.basename(blosum_filename))[0]
    if blosum_base.startswith("blosum"):
        suffix = blosum_base[6:]
    else:
        suffix = blosum_base

    # Standard Newick (leaves only)
    newick_str = to_newick(tree_root) + ";"
    newick_path = f"tree_blosum{suffix}_newick.nw"
    with open(newick_path, "w", encoding="utf-8") as f:
        f.write(newick_str)
    print(f"Tree saved in Newick format (leaves only) to {newick_path}")

    # Newick with distances
    newick_dist_str = to_newick_with_distances(tree_root) + ";"
    newick_dist_path = f"tree_blosum{suffix}_newick_with_distance.nw"
    with open(newick_dist_path, "w", encoding="utf-8") as f:
        f.write(newick_dist_str)
    print(f"Tree saved in Newick format (with distances) to {newick_dist_path}")


def read_thresholds(filepath: str) -> List[int]:
    thresholds = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                thresholds.append(int(line))
    return thresholds


def save_clusters_to_json(
    clusters_by_threshold: Dict[int, List[List[str]]], blosum_filename: str
):
    blosum_base = os.path.splitext(os.path.basename(blosum_filename))[0]
    if blosum_base.startswith("blosum"):
        suffix = blosum_base[6:]
    else:
        suffix = blosum_base
    output_filename = f"clusters_for_blosum{suffix}.json"
    output_path = os.path.join(output_filename)
    # Convert keys to strings for JSON compatibility
    clusters_by_threshold_str_keys = {str(k): v for k, v in clusters_by_threshold.items()}
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(clusters_by_threshold_str_keys, f, indent=2)
    print(f"Clusters saved to {output_path}")


def main():
    organisms_path = os.path.join("organisms.json")
    blosum_path = os.path.join("blosum62.json")  # Replace XX as needed

    sequences = load_sequences(organisms_path)
    blosum = load_blosum(blosum_path)

    pairwise_scores = compute_all_pairwise_scores(sequences, blosum)
    flat_scores = flatten_scores(pairwise_scores)
    save_scores_to_json(flat_scores, blosum_path)

    species = list(sequences.keys())
    tree_root = build_phylogenetic_tree(species, flat_scores)

    print("Phylogenetic tree root node:")
    print(tree_root)

    # Save Newick files
    save_newick_files(tree_root, blosum_path)

    # Draw and save dendrogram
    blosum_base = os.path.splitext(os.path.basename(blosum_path))[0]
    if blosum_base.startswith("blosum"):
        suffix = blosum_base[6:]
    else:
        suffix = blosum_base
    dendrogram_filename = f"phylogenetic_tree_blosum{suffix}.png"
    draw_dendrogram(tree_root, dendrogram_filename)

    # Read thresholds and compute clusters
    thresholds_path = os.path.join("thresholds.txt")
    thresholds = read_thresholds(thresholds_path)
    clusters_by_threshold = {}
    for threshold in thresholds:
        clusters = get_clusters_below_threshold(tree_root, threshold)
        clusters_by_threshold[threshold] = clusters
        print(f"Threshold {threshold}:")
        for i, cluster in enumerate(clusters, 1):
            print(f"  Cluster {i}: {cluster}")

    save_clusters_to_json(clusters_by_threshold, blosum_path)


if __name__ == "__main__":
    main()