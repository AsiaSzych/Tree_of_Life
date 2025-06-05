# main.py

import os
import json
from typing import Dict, Tuple, List

# Import functions/classes from your src modules
from src.aligner import NeedlemanWunschAligner
from src.data_io import (
    load_organisms,
    save_pairwise_scores,
    load_thresholds,
    save_newick_tree,
    save_clusters
)
from src.tree_logic import TreeNode, build_phylogenetic_tree, generate_newick
from src.clustering_logic import extract_clusters
from src.visualization import draw_and_save_dendrogram


def main():
    """
    Main function to orchestrate the DNA sequence alignment, phylogenetic tree building,
    and clustering process.
    """
    # Define file paths relative to the current directory, using subfolders
    ORGANISMS_FILE = os.path.join("data", "organisms.json")
    THRESHOLDS_FILE = os.path.join("data", "thresholds.txt")

    # --- Configuration for BLOSUM file ---
    # Choose which BLOSUM matrix to use for this run.
    # Uncomment one of the following lines to switch between BLOSUM versions.
    # For the provided test case, use "blosum_test.json".
    # BLOSUM_FILENAME = "blosum_test.json"  # For the specific test case
    # BLOSUM_FILENAME = "blosum50.json"   # For general use with BLOSUM50
    BLOSUM_FILENAME = "blosum62.json"   # For general use with BLOSUM62

    BLOSUM_FILE = os.path.join("data", BLOSUM_FILENAME)

    # Determine the suffix for the output file based on the BLOSUM filename
    blosum_suffix = BLOSUM_FILENAME.replace("blosum", "").replace(".json", "")
    OUTPUT_SCORES_FILE = os.path.join("output", f"organisms_scores_blosum{blosum_suffix}.json")
    OUTPUT_NEWICK_FILE = os.path.join("output", f"tree{blosum_suffix}_newick.nw")
    OUTPUT_NEWICK_DIST_FILE = os.path.join("output", f"tree{blosum_suffix}_newick_with_distance.nw")
    OUTPUT_DENDROGRAM_FILE = os.path.join("output", f"phylogenetic_tree_blosum{blosum_suffix}.png")
    OUTPUT_CLUSTERS_FILE = os.path.join("output", f"clusters_for_blosum{blosum_suffix}.json")

    print(f"--- Starting Needleman-Wunsch Alignment, Tree Building, and Clustering ---")
    print(f"Attempting to load organisms from: {ORGANISMS_FILE}")
    try:
        organisms_data = load_organisms(ORGANISMS_FILE)
        print(f"Successfully loaded {len(organisms_data)} organisms.")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error loading organisms data: {e}")
        print("Please ensure 'data/organisms.json' exists and is correctly formatted.")
        return

    print(f"\nInitializing Needleman-Wunsch aligner with BLOSUM from: {BLOSUM_FILE}")
    try:
        aligner = NeedlemanWunschAligner(BLOSUM_FILE)
        print("Aligner initialized successfully.")
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        print(f"Error initializing aligner: {e}")
        print(f"Please ensure '{BLOSUM_FILE}' exists and is correctly formatted.")
        return

    print("\n--- Calculating all pairwise Needleman-Wunsch scores ---")
    # This function was previously part of the main script, but it's a higher-level
    # operation that uses the aligner. We'll keep it here for now or move it to a
    # dedicated 'processing' module if the project grows.
    species_names = list(organisms_data.keys())
    num_species = len(species_names)
    pairwise_scores: Dict[Tuple[str, str], int] = {}

    print(f"Calculating scores for {num_species * (num_species - 1) // 2} unique pairs...")

    for i in range(num_species):
        for j in range(i + 1, num_species):
            species1_name = species_names[i]
            species2_name = species_names[j]
            seq1 = organisms_data[species1_name]
            seq2 = organisms_data[species2_name]

            try:
                score = aligner.align(seq1, seq2)
                pairwise_scores[tuple(sorted((species1_name, species2_name)))] = score
                print(f"  Score for ({species1_name}, {species2_name}): {score}")
            except ValueError as e:
                print(f"  Error aligning ({species1_name}, {species2_name}): {e}")
            except Exception as e:
                print(f"  An unexpected error occurred aligning ({species1_name}, {species2_name}): {e}")

    print("\n--- All pairwise scores calculated ---")
    if pairwise_scores:
        for (s1, s2), score in pairwise_scores.items():
            print(f"  {s1} vs {s2}: {score}")
    else:
        print("No scores were calculated. This might happen if there are fewer than two species or errors occurred.")

    print("\n--- Saving calculated scores ---")
    try:
        save_pairwise_scores(pairwise_scores, OUTPUT_SCORES_FILE)
    except IOError:
        print("Failed to save scores. Please check file permissions or disk space.")
        return

    print("\n--- Building Phylogenetic Tree ---")
    try:
        species_names_list = sorted(list(organisms_data.keys()))
        root_node, linkage_matrix, _ = build_phylogenetic_tree(pairwise_scores, species_names_list)
        print("Phylogenetic tree built successfully.")
    except ValueError as e:
        print(f"Error building phylogenetic tree: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during tree building: {e}")
        return

    print("\n--- Generating and Saving Newick Formats ---")
    try:
        newick_no_dist = generate_newick(root_node, include_distances=False)
        save_newick_tree(newick_no_dist, OUTPUT_NEWICK_FILE)

        newick_with_dist = generate_newick(root_node, include_distances=True)
        save_newick_tree(newick_with_dist, OUTPUT_NEWICK_DIST_FILE)
    except Exception as e:
        print(f"Error generating or saving Newick files: {e}")
        return

    print("\n--- Drawing and Saving Dendrogram ---")
    try:
        draw_and_save_dendrogram(
            linkage_matrix,
            species_names_list,
            OUTPUT_DENDROGRAM_FILE,
            title=f"Phylogenetic Tree (BLOSUM{blosum_suffix})"
        )
    except Exception as e:
        print(f"Failed to draw or save dendrogram: {e}")
        return

    print("\n--- Extracting and Saving Clusters ---")
    try:
        thresholds = load_thresholds(THRESHOLDS_FILE)
        if not thresholds:
            print(f"No thresholds found in '{THRESHOLDS_FILE}'. Skipping cluster extraction.")
            return

        all_clusters_by_threshold: Dict[str, List[List[str]]] = {}
        for threshold in thresholds:
            print(f"\n  Clustering for threshold: {threshold}")
            clusters = extract_clusters(linkage_matrix, species_names_list, threshold)
            all_clusters_by_threshold[str(threshold)] = clusters

            for i, cluster in enumerate(clusters):
                print(f"    Cluster {i+1}: {', '.join(cluster)}")

        save_clusters(all_clusters_by_threshold, OUTPUT_CLUSTERS_FILE)

    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"Error during cluster extraction or saving: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during clustering: {e}")
        return

    print("\n--- All Tasks Complete ---")


if __name__ == "__main__":
    # --- Setup for testing: Create dummy data files ---
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    main()