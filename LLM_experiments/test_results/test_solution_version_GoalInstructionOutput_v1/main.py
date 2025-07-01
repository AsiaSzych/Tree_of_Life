from pathlib import Path

from src.utils.file_io import (
    load_sequences, load_scoring_matrix, save_scores_to_json,
    load_scores_from_json, save_text_file, load_thresholds, save_clusters_to_json
)
from src.alignment.needleman_wunsch import calculate_alignment_score
from src.clustering.hierarchical import build_tree, to_newick, get_clusters_by_threshold
from src.visualization.dendrogram import plot_dendrogram
import itertools

# --- Configuration ---
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
ORGANISMS_FILE = DATA_DIR / "organisms.json"
# Choose which BLOSUM matrix to use by changing the filename
SCORING_FILE = DATA_DIR / "blosum62.json"
# SCORING_FILE = DATA_DIR / "blosum50.json"
THRESHOLDS_FILE = DATA_DIR / "thresholds.txt"


def run_pairwise_alignment():
    """
    Step 1 of the pipeline: Calculate and save pairwise alignment scores.
    """
    print("--- Starting Pairwise Alignment ---")
    sequences = load_sequences(ORGANISMS_FILE)
    scoring_matrix = load_scoring_matrix(SCORING_FILE)

    if not sequences or not scoring_matrix:
        print("Could not load data for alignment. Exiting.")
        return None

    species_names = list(sequences.keys())
    alignment_scores = {name: {} for name in species_names}

    print("Calculating alignment scores...")
    for species1, species2 in itertools.combinations(species_names, 2):
        score = calculate_alignment_score(sequences[species1], sequences[species2], scoring_matrix)
        alignment_scores[species1][species2] = score
        alignment_scores[species2][species1] = score

    output_filename = f"organisms_scores_{SCORING_FILE.stem}.json"
    save_scores_to_json(alignment_scores, species_names, OUTPUT_DIR / output_filename)
    return alignment_scores


def run_tree_construction():
    """
    Step 2 of the pipeline: Load scores and build the hierarchical tree.
    """
    print("\n--- Starting Tree Construction ---")
    scores_filename = f"organisms_scores_{SCORING_FILE.stem}.json"
    scores_filepath = OUTPUT_DIR / scores_filename
    scores, labels = load_scores_from_json(scores_filepath)

    if not scores:
        print("Scores could not be loaded. Please run the alignment step first.")
        return None

    print("Building hierarchical tree...")
    linkage_matrix, max_similarity = build_tree(scores, labels)
    print("Tree construction complete.")
    return linkage_matrix, labels, max_similarity


def run_full_pipeline():
    """
    Runs the entire project pipeline from tree construction to final analysis.
    Assumes the scores file from `run_pairwise_alignment` already exists.
    """
    print("\n--- Starting Full Project Pipeline ---")

    # 1. Build the tree
    tree_data = run_tree_construction()
    if not tree_data:
        print("Pipeline halted: Could not build tree.")
        return
    linkage_matrix, labels, max_similarity = tree_data

    # 2. Run Exports and Visualizations
    print("\n--- Generating Newick Formats and Dendrogram ---")
    # Newick Export
    newick_simple = to_newick(linkage_matrix, labels, with_distance=False)
    save_text_file(newick_simple, OUTPUT_DIR / f"tree_{SCORING_FILE.stem}_newick.nw")
    newick_with_dist = to_newick(linkage_matrix, labels, with_distance=True)
    save_text_file(newick_with_dist, OUTPUT_DIR / f"tree_{SCORING_FILE.stem}_newick_with_distance.nw")

    # Dendrogram Plot
    dendrogram_filepath = OUTPUT_DIR / f"phylogenetic_tree_{SCORING_FILE.stem}.png"
    plot_dendrogram(linkage_matrix, labels, max_similarity, dendrogram_filepath)

    # 3. Cluster Extraction
    print("\n--- Starting Cluster Extraction by Threshold ---")
    thresholds = load_thresholds(THRESHOLDS_FILE)
    if not thresholds:
        print("No thresholds found. Skipping cluster extraction.")
        return

    all_clusters = {}
    print("Calculating clusters for each threshold...")
    for threshold in thresholds:
        clusters = get_clusters_by_threshold(linkage_matrix, labels, threshold, max_similarity)
        all_clusters[threshold] = clusters
        print(f"\nThreshold: {threshold}")
        for i, cluster in enumerate(clusters):
            print(f"  - Cluster {i+1}: {cluster}")

    # 4. Save the final cluster data
    cluster_filename = f"clusters_for_{SCORING_FILE.stem}.json"
    save_clusters_to_json(all_clusters, OUTPUT_DIR / cluster_filename)


if __name__ == "__main__":
    # To run the project, you may need to run alignment first if the scores file is missing.
    print(">>> STEP 1: Running Pairwise Alignment (if needed)")
    run_pairwise_alignment()

    print("\n>>> FINAL STEP: Running Full Analysis Pipeline")
    run_full_pipeline()