import os
import json
import re
from src.tree import (
    build_similarity_tree,
    TreeNode,
    plot_dendrogram,
    get_clusters_at_threshold,
)

def load_similarity_scores(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def save_newick(tree: TreeNode, filepath: str, with_distances: bool = False):
    if with_distances:
        newick_str = tree.to_newick_with_distances() + ";"
    else:
        newick_str = tree.to_newick() + ";"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(newick_str)

def load_thresholds(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as f:
        return [int(line.strip()) for line in f if line.strip()]

def load_organisms(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_blosum(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: int(v) for k, v in raw.items()}

def needleman_wunsch(seq1: str, seq2: str, blosum: dict) -> int:
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + blosum[seq1[i - 1]]
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + blosum[seq2[j - 1]]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            char1 = seq1[i - 1]
            char2 = seq2[j - 1]
            match_key = char1 + char2
            match_score = blosum[match_key]
            delete_score = blosum[char1]
            insert_score = blosum[char2]
            dp[i][j] = max(
                dp[i - 1][j - 1] + match_score,
                dp[i - 1][j] + delete_score,
                dp[i][j - 1] + insert_score
            )
    return dp[m][n]

def compute_all_pairwise_scores(organisms: dict, blosum: dict) -> dict:
    species = list(organisms.keys())
    scores = {}
    for i, sp1 in enumerate(species):
        seq1 = organisms[sp1]
        for j, sp2 in enumerate(species):
            if i > j:
                continue  # Avoid duplicate pairs
            seq2 = organisms[sp2]
            score = needleman_wunsch(seq1, seq2, blosum)
            key = f"{sp1}_{sp2}" if sp1 <= sp2 else f"{sp2}_{sp1}"
            scores[key] = score
    return scores

def main():
    # Set these paths as needed
    data_dir = "data"
    organisms_path = os.path.join(data_dir, "organisms.json")
    blosum_path = os.path.join(data_dir, "blosum62.json")  # Change to blosum62.json as needed
    thresholds_path = os.path.join(data_dir, "thresholds.txt")

    # Extract BLOSUM version from filename
    match = re.search(r"blosum(\d+)", os.path.basename(blosum_path))
    blosum_version = match.group(1) if match else "XX"

    # Output file paths
    scores_path = os.path.join(data_dir, f"organisms_scores_blosum{blosum_version}.json")
    newick_path = os.path.join(data_dir, f"tree_blosum{blosum_version}_newick.nw")
    newick_dist_path = os.path.join(data_dir, f"tree_blosum{blosum_version}_newick_with_distance.nw")
    dendrogram_path = os.path.join(data_dir, f"phylogenetic_tree_blosum{blosum_version}.png")
    clusters_path = os.path.join(data_dir, f"clusters_for_blosum{blosum_version}.json")

    # Step 1: Load input data
    organisms = load_organisms(organisms_path)
    blosum = load_blosum(blosum_path)

    # Step 2: Compute and save all pairwise Needleman-Wunsch scores
    scores = compute_all_pairwise_scores(organisms, blosum)
    with open(scores_path, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

    # Step 3: Build the phylogenetic tree
    root = build_similarity_tree(scores)

    # Step 4: Save tree in Newick formats
    save_newick(root, newick_path, with_distances=False)
    save_newick(root, newick_dist_path, with_distances=True)

    # Step 5: Save dendrogram
    plot_dendrogram(root, dendrogram_path)

    # Step 6: Load thresholds and compute clusters
    thresholds = load_thresholds(thresholds_path)
    clusters_for_thresholds = {}
    for threshold in thresholds:
        clusters = get_clusters_at_threshold(root, threshold)
        clusters_for_thresholds[threshold] = clusters
        print(f"Threshold: {threshold}")
        for i, cluster in enumerate(clusters, 1):
            print(f"  Cluster {i}: {cluster}")

    # Step 7: Save clusters to JSON
    with open(clusters_path, "w", encoding="utf-8") as f:
        json.dump(clusters_for_thresholds, f, indent=2)

    print(f"Pairwise scores saved to: {scores_path}")
    print(f"Tree saved in Newick format to: {newick_path}")
    print(f"Tree with distances saved in Newick format to: {newick_dist_path}")
    print(f"Dendrogram saved to: {dendrogram_path}")
    print(f"Clusters for thresholds saved to: {clusters_path}")

if __name__ == "__main__":
    main()