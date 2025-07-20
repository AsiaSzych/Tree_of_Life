import os
import re
import json
from needleman_wunsch import load_organisms, load_blosum, compute_all_pairwise_scores, save_scores_to_json
from phylo_tree import build_phylogenetic_tree, TreeNode
from newick_export import save_newick_files
from dendrogram_draw import plot_dendrogram
from tree_clustering import read_thresholds, get_all_clusters, save_clusters_to_json

def load_similarity_scores(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_blosum_number(blosum_filename: str) -> str:
    import re
    match = re.search(r"blosum(\d+)", blosum_filename)
    if match:
        return match.group(1)
    raise ValueError("BLOSUM filename must contain a number, e.g., 'blosum50.json'.")

def main():
     # Set paths relative to current directory
    organisms_path = os.path.join("organisms.json")
    blosum_path = os.path.join("blosum62.json")  # Replace XX with 50 or 62 as needed

    organisms = load_organisms(organisms_path)
    blosum = load_blosum(blosum_path)

    scores = compute_all_pairwise_scores(organisms, blosum)

    # Determine output filename based on BLOSUM matrix used
    blosum_number = extract_blosum_number(os.path.basename(blosum_path))
    output_filename = f"organisms_scores_blosum{blosum_number}.json"
    output_path = os.path.join(output_filename)

    save_scores_to_json(scores, output_path)

    print(f"Pairwise Needleman-Wunsch scores saved to {output_path}")
    
    scores_path = os.path.join("organisms_scores_blosum62.json")  # Replace XX as needed
    thresholds_path = os.path.join("thresholds.txt")

    organisms = load_organisms(organisms_path)
    species = list(organisms.keys())
    similarity_scores = load_similarity_scores(scores_path)

    root = build_phylogenetic_tree(similarity_scores, species)

    # Extract BLOSUM version from file name
    blosum_version = extract_blosum_number(scores_path)

    # Save Newick files
    save_newick_files(root, blosum_version)

    # Draw and save dendrogram
    plot_dendrogram(root, blosum_version)

    # Read thresholds and compute clusters
    thresholds = read_thresholds(thresholds_path)
    clusters = get_all_clusters(root, thresholds)

    # Print clusters to standard output
    for t in thresholds:
        print(f"Threshold {t}:")
        for idx, cluster in enumerate(clusters[t], 1):
            print(f"  Cluster {idx}: {cluster}")

    # Save clusters to JSON
    save_clusters_to_json(clusters, blosum_version)

    print(
        f"Tree saved to tree_blosum{blosum_version}_newick.nw, "
        f"tree_blosum{blosum_version}_newick_with_distance.nw, "
        f"phylogenetic_tree_blosum{blosum_version}.png, "
        f"and clusters_for_blosum{blosum_version}.json"
    )

if __name__ == "__main__":
    main()