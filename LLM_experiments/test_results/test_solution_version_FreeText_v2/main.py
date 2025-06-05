# main.py
import os
import json
import re
from typing import Dict, List, Tuple
from collections import defaultdict

from src.utils import load_json_data, save_json_data
from src.aligner import NeedlemanWunschAligner
from src.tree_builder import PhylogeneticTreeBuilder
from src.tree_exporter import TreeExporter
from src.visualizer import DendrogramVisualizer # Import new visualizer
from src.cluster_analyzer import ClusterAnalyzer # Import new cluster analyzer

def calculate_pairwise_alignment_scores(
    organisms_filepath: str,
    blosum_matrix_filepath: str
) -> Dict[str, Dict[str, int]]:
    """
    Calculates Needleman-Wunsch similarity scores for all unique pairs of species.

    Args:
        organisms_filepath (str): Path to the JSON file containing species DNA sequences.
        blosum_matrix_filepath (str): Path to the JSON file containing the BLOSUM-like matrix.

    Returns:
        Dict[str, Dict[str, int]]: A nested dictionary where
                                   scores[species1][species2] holds the alignment score.
                                   The matrix is symmetric (score(A,B) == score(B,A)).
                                   Diagonal elements (score(A,A)) are also included.
    """
    print(f"Loading organisms from: {organisms_filepath}")
    organisms_data = load_json_data(organisms_filepath)

    if not isinstance(organisms_data, dict):
        raise ValueError(
            f"Invalid organisms data format in '{organisms_filepath}': "
            "Expected a dictionary."
        )

    species_list: List[Tuple[str, str]] = list(organisms_data.items())
    num_species = len(species_list)

    if num_species == 0:
        print("No species found in the organisms file. Exiting.")
        return {}

    print(f"Initializing Needleman-Wunsch aligner with matrix: {blosum_matrix_filepath}")
    aligner = NeedlemanWunschAligner(blosum_matrix_filepath)

    pairwise_scores: Dict[str, Dict[str, int]] = defaultdict(dict)

    print(f"Calculating pairwise alignment scores for {num_species} species...")

    for i in range(num_species):
        species1_name, dna1 = species_list[i]
        if species1_name not in pairwise_scores[species1_name]:
            score_self = aligner.align(dna1, dna1)
            pairwise_scores[species1_name][species1_name] = score_self
            # print(f"  Score({species1_name}, {species1_name}): {score_self}")

        for j in range(i + 1, num_species):
            species2_name, dna2 = species_list[j]
            score = aligner.align(dna1, dna2)
            pairwise_scores[species1_name][species2_name] = score
            pairwise_scores[species2_name][species1_name] = score

            # print(f"  Score({species1_name}, {species2_name}): {score}")

    print("Pairwise alignment score calculation complete.")
    return pairwise_scores

def prepare_and_save_scores(
    pairwise_scores: Dict[str, Dict[str, int]],
    blosum_matrix_filepath: str,
    output_dir: str
) -> str:
    """
    Prepares the pairwise scores into the required flat format and saves them to a JSON file.

    Args:
        pairwise_scores (Dict[str, Dict[str, int]]): The nested dictionary of scores.
        blosum_matrix_filepath (str): The path to the BLOSUM matrix file used,
                                      to determine the output filename.
        output_dir (str): The directory where the output JSON file should be saved.

    Returns:
        str: The full path to the saved scores file.
    """
    flat_scores: Dict[str, int] = {}
    for species1, inner_dict in pairwise_scores.items():
        for species2, score in inner_dict.items():
            if species1 <= species2:
                key = f"{species1}_{species2}"
                flat_scores[key] = int(score)

    match = re.search(r'blosum(\d+)\.json$', blosum_matrix_filepath)
    if not match:
        raise ValueError(
            f"Could not extract BLOSUM version from filename: {blosum_matrix_filepath}. "
            "Expected format like 'blosumXX.json'."
        )
    blosum_version = match.group(1)
    output_filename = f"organisms_scores_blosum{blosum_version}.json"
    output_filepath = os.path.join(output_dir, output_filename)

    save_json_data(flat_scores, output_filepath)
    return output_filepath


if __name__ == "__main__":
    # Define paths relative to the current directory
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
    ORGANISMS_FILE = os.path.join(DATA_DIR, 'organisms.json')
    BLOSUM50_FILE = os.path.join(DATA_DIR, 'blosum50.json')
    BLOSUM62_FILE = os.path.join(DATA_DIR, 'blosum62.json')
    THRESHOLDS_FILE = os.path.join(DATA_DIR, 'thresholds.txt') # New thresholds file

    # --- Create dummy data files for testing ---
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        # --- Needleman-Wunsch Score Calculation and Saving ---
        print("\n--- Calculating and Saving Needleman-Wunsch Scores ---")

        # Run with the  BLOSUM50 matrix and original organisms
        all_pairwise_scores_50 = calculate_pairwise_alignment_scores(
            organisms_filepath=ORGANISMS_FILE,
            blosum_matrix_filepath=BLOSUM50_FILE
        )
        scores_50_filepath = prepare_and_save_scores(all_pairwise_scores_50, BLOSUM50_FILE, OUTPUT_DIR)
        print(f"BLOSUM50 scores saved to: {scores_50_filepath}")

        # Run with the general BLOSUM62 matrix
        all_pairwise_scores_62 = calculate_pairwise_alignment_scores(
            organisms_filepath=ORGANISMS_FILE,
            blosum_matrix_filepath=BLOSUM62_FILE
        )
        scores_62_filepath = prepare_and_save_scores(all_pairwise_scores_62, BLOSUM62_FILE, OUTPUT_DIR)
        print(f"BLOSUM62 scores saved to: {scores_62_filepath}")

        # --- Phylogenetic Tree Building ---
        print("\n--- Building Phylogenetic Trees ---")

        # Build tree for BLOSUM50 scores
        print(f"\nBuilding tree for scores from: {scores_50_filepath}")
        tree_builder_50 = PhylogeneticTreeBuilder(scores_50_filepath)
        linkage_matrix_50, species_labels_50, max_sim_50 = tree_builder_50.build_tree()
        print(f"Linkage Matrix (BLOSUM50):\n{linkage_matrix_50}")
        print(f"Species Labels (BLOSUM50): {species_labels_50}")
        print(f"Max Similarity Score (BLOSUM50): {max_sim_50}")

        # Build tree for BLOSUM62 scores
        print(f"\nBuilding tree for scores from: {scores_62_filepath}")
        tree_builder_62 = PhylogeneticTreeBuilder(scores_62_filepath)
        linkage_matrix_62, species_labels_62, max_sim_62 = tree_builder_62.build_tree()
        print(f"Linkage Matrix (BLOSUM62):\n{linkage_matrix_62}")
        print(f"Species Labels (BLOSUM62): {species_labels_62}")
        print(f"Max Similarity Score (BLOSUM62): {max_sim_62}")

        # --- Exporting Trees to Newick Format ---
        print("\n--- Exporting Trees to Newick Format ---")
        tree_exporter = TreeExporter(OUTPUT_DIR)

        # Export for BLOSUM50
        print("\nExporting BLOSUM50 tree...")
        tree_exporter.export_to_newick(
            linkage_matrix=linkage_matrix_50,
            species_labels=species_labels_50,
            blosum_matrix_filepath=BLOSUM50_FILE
        )

        # Export for BLOSUM62
        print("\nExporting BLOSUM62 tree...")
        tree_exporter.export_to_newick(
            linkage_matrix=linkage_matrix_62,
            species_labels=species_labels_62,
            blosum_matrix_filepath=BLOSUM62_FILE
        )

        # --- Drawing Dendrograms ---
        print("\n--- Drawing Dendrograms ---")
        dendrogram_visualizer = DendrogramVisualizer(OUTPUT_DIR)

        # Draw for BLOSUM50
        print("\nDrawing BLOSUM50 dendrogram...")
        dendrogram_visualizer.draw_and_save_dendrogram(
            linkage_matrix=linkage_matrix_50,
            species_labels=species_labels_50,
            blosum_matrix_filepath=BLOSUM50_FILE,
            max_similarity_score=max_sim_50
        )

        # Draw for BLOSUM62
        print("\nDrawing BLOSUM62 dendrogram...")
        dendrogram_visualizer.draw_and_save_dendrogram(
            linkage_matrix=linkage_matrix_62,
            species_labels=species_labels_62,
            blosum_matrix_filepath=BLOSUM62_FILE,
            max_similarity_score=max_sim_62
        )

        # --- Finding and Saving Clusters ---
        print("\n--- Finding and Saving Clusters ---")
        cluster_analyzer = ClusterAnalyzer(OUTPUT_DIR)

        # Analyze and save clusters for BLOSUM50
        cluster_analyzer.find_and_save_clusters(
            linkage_matrix=linkage_matrix_50,
            species_labels=species_labels_50,
            max_similarity_score=max_sim_50,
            thresholds_filepath=THRESHOLDS_FILE,
            blosum_matrix_filepath=BLOSUM50_FILE
        )

        # Analyze and save clusters for BLOSUM62
        cluster_analyzer.find_and_save_clusters(
            linkage_matrix=linkage_matrix_62,
            species_labels=species_labels_62,
            max_similarity_score=max_sim_62,
            thresholds_filepath=THRESHOLDS_FILE,
            blosum_matrix_filepath=BLOSUM62_FILE
        )


    except (FileNotFoundError, ValueError, json.JSONDecodeError, IOError, Exception) as e:
        print(f"\nAn error occurred: {e}")