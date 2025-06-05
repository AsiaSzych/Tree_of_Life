# main.py

import os
from src.utils import load_json_data, save_json_data
from src.alignment import calculate_all_pairwise_scores, needleman_wunsch, _parse_blosum_scores
from src.tree_builder import build_phylogenetic_tree, export_tree_to_newick, draw_and_save_dendrogram
from src.clustering import load_thresholds, get_clusters_at_threshold # New imports
from typing import Dict, List, Tuple, Any
import numpy as np

def main():
    """
    Main function to orchestrate loading data, calculating Needleman-Wunsch scores,
    saving scores, building the phylogenetic tree, exporting it to Newick format,
    drawing the dendrogram, and performing threshold-based clustering.
    """
    # Define file paths relative to the current working directory
    DATA_DIR = "data"
    OUTPUT_DIR = "output"

    ORGANISMS_FILE = os.path.join(DATA_DIR, "organisms.json")
    BLOSUM_50_FILE = os.path.join(DATA_DIR, "blosum50.json")
    BLOSUM_62_FILE = os.path.join(DATA_DIR, "blosum62.json")
    THRESHOLDS_FILE = os.path.join(DATA_DIR, "thresholds.txt") # New input file

    print("--- Starting Full Phylogenetic Analysis and Clustering ---")

    # --- Step 1: Load Organisms Data ---
    try:
        organisms_data: Dict[str, str] = load_json_data(ORGANISMS_FILE)
        print(f"\nSuccessfully loaded organisms data from '{ORGANISMS_FILE}'.")
    except Exception as e:
        print(e)
        print("Please ensure 'data/organisms.json' exists and is correctly formatted.")
        return

    # --- Step 2: Choose and Load BLOSUM Data ---
    # For this run, let's use BLOSUM50 as an example.
    # To switch, change BLOSUM_FILE_TO_USE to BLOSUM_62_FILE
    BLOSUM_FILE_TO_USE = BLOSUM_50_FILE
    try:
        blosum_data: Dict[str, int] = load_json_data(BLOSUM_FILE_TO_USE)
        print(f"Successfully loaded BLOSUM data from '{BLOSUM_FILE_TO_USE}'.")
    except Exception as e:
        print(e)
        print(f"Please ensure '{BLOSUM_FILE_TO_USE}' exists and is correctly formatted.")
        return

    # --- Step 3: Calculate and Save Pairwise Needleman-Wunsch Scores (if not already done) ---
    print("\nPreparing pairwise Needleman-Wunsch scores...")

    blosum_filename = os.path.basename(BLOSUM_FILE_TO_USE)
    blosum_suffix = blosum_filename.replace("blosum", "").replace(".json", "")
    output_scores_filename = f"organisms_scores_blosum{blosum_suffix}.json"
    output_scores_filepath = os.path.join(OUTPUT_DIR, output_scores_filename)

    pairwise_scores_for_tree: Dict[str, int] = {}
    if os.path.exists(output_scores_filepath):
        print(f"Attempting to load existing pairwise scores from '{output_scores_filepath}'.")
        try:
            pairwise_scores_for_tree = load_json_data(output_scores_filepath)
            print("Existing scores loaded successfully.")
        except Exception as e:
            print(f"Error loading existing scores: {e}. Recalculating scores.")
    
    if not pairwise_scores_for_tree: # If file didn't exist or loading failed
        print("Recalculating all pairwise Needleman-Wunsch scores...")
        try:
            in_memory_pairwise_scores = calculate_all_pairwise_scores(organisms_data, blosum_data)
            flat_scores_to_save: Dict[str, int] = {}
            processed_pairs = set()

            for species1, inner_dict in in_memory_pairwise_scores.items():
                for species2, score in inner_dict.items():
                    sorted_names = tuple(sorted([species1, species2]))
                    key = f"{sorted_names[0]}_{sorted_names[1]}"
                    if key not in processed_pairs:
                        flat_scores_to_save[key] = score
                        processed_pairs.add(key)
            
            save_json_data(output_scores_filepath, flat_scores_to_save)
            pairwise_scores_for_tree = flat_scores_to_save
            print(f"Successfully calculated and saved pairwise scores to '{output_scores_filepath}'.")
        except Exception as e:
            print(f"Error during score calculation or saving: {e}")
            return
    
    # --- Step 4: Build Phylogenetic Tree ---
    print("\nBuilding phylogenetic tree using single-linkage clustering...")
    linkage_matrix: np.ndarray
    species_labels: List[str]
    max_similarity: int
    try:
        linkage_matrix, species_labels, max_similarity = build_phylogenetic_tree(
            organisms_data, pairwise_scores_for_tree
        )
        print("\nPhylogenetic tree (linkage matrix) successfully built.")
        if linkage_matrix.shape[0] > 0:
            root_merge_distance = linkage_matrix[-1, 2]
            root_merge_similarity = max_similarity - root_merge_distance
            print(f"\nRoot node (final merge) formed at a similarity score of: {root_merge_similarity}")
            print(f"This corresponds to a distance of: {root_merge_distance}")

    except ValueError as e:
        print(f"Error building tree: {e}")
        print("Please ensure your pairwise scores file is complete and correctly formatted, "
              "and covers all species in 'organisms.json'.")
        return
    except Exception as e:
        print(f"An unexpected error occurred during tree building: {e}")
        return

    # --- Step 5: Export Tree to Newick Format ---
    # print("\nExporting phylogenetic tree to Newick format...")
    # try:
    #     export_tree_to_newick(linkage_matrix, species_labels, OUTPUT_DIR, blosum_suffix)
    # except Exception as e:
    #     print(f"Error during Newick export: {e}")
    #     return

    # --- Step 6: Draw and Save Dendrogram ---
    print("\nDrawing and saving dendrogram...")
    try:
        draw_and_save_dendrogram(linkage_matrix, species_labels, OUTPUT_DIR, blosum_suffix)
    except Exception as e:
        print(f"Error during dendrogram drawing: {e}")
        return

    # --- Step 7: Perform Clustering based on Thresholds ---
    print("\n--- Performing Clustering ---")
    output_clusters_filename = f"clusters_for_blosum{blosum_suffix}.json"
    output_clusters_filepath = os.path.join(OUTPUT_DIR, output_clusters_filename)
    
    try:
        thresholds = load_thresholds(THRESHOLDS_FILE)
        print(f"Loaded thresholds from '{THRESHOLDS_FILE}': {thresholds}")
    except Exception as e:
        print(f"Error loading thresholds: {e}")
        print("Please ensure 'data/thresholds.txt' exists and contains valid numbers.")
        return

    all_clusters_by_threshold: Dict[str, List[List[str]]] = {}

    for threshold in thresholds:
        print(f"\n--- Clusters for threshold: {threshold} ---")
        try:
            clusters = get_clusters_at_threshold(linkage_matrix, species_labels, threshold)
            all_clusters_by_threshold[str(threshold)] = clusters # JSON keys must be strings
            for i, cluster in enumerate(clusters):
                print(f"  Cluster {i+1}: {cluster}")
        except Exception as e:
            print(f"Error calculating clusters for threshold {threshold}: {e}")
            # Continue to next threshold even if one fails

    # Save all clusters to a JSON file
    try:
        save_json_data(output_clusters_filepath, all_clusters_by_threshold)
        print(f"\nAll clusters saved to '{output_clusters_filepath}'.")
    except Exception as e:
        print(f"Error saving clusters to file: {e}")

    # --- Step 8: Run Exemplary Needleman-Wunsch Test Case (kept for continuity) ---
    print("\n--- Running Exemplary Needleman-Wunsch Test Case ---")
    test_seq1 = "aabaab"
    test_seq2 = "ababaa"
    test_blosum_data = {"a": -1, "b": -2, "ab": -3, "ba": -3, "aa": 2, "bb": 3}
    expected_output = 7

    try:
        test_sub_matrix, test_gap_penalties = _parse_blosum_scores(test_blosum_data)
        actual_output = needleman_wunsch(test_seq1, test_seq2, test_sub_matrix, test_gap_penalties)

        print(f"Test Case: seq1='{test_seq1}', seq2='{test_seq2}'")
        print(f"BLOSUM data: {test_blosum_data}")
        print(f"Expected NW score: {expected_output}")
        print(f"Actual NW score:   {actual_output}")

        if actual_output == expected_output:
            print("Test Case PASSED!")
        else:
            print("Test Case FAILED!")
            print(f"Discrepancy: Expected {expected_output}, Got {actual_output}")

    except ValueError as e:
        print(f"Error in test case: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during test case execution: {e}")

    print("\n--- Full Phylogenetic Analysis and Clustering Complete ---")


if __name__ == "__main__":
    main()
