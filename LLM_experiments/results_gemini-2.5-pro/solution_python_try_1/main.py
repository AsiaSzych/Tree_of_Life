import json
from pathlib import Path
from typing import Dict, Any, List

from src.clustering import (
    build_tree_from_scores,
    convert_tree_to_newick,
    get_clusters_by_threshold
)
from src.visualization import plot_dendrogram

# --- Configuration ---
DATA_DIR = Path("data")
OUTPUT_DIR = Path("results")
ORGANISMS_FILE = DATA_DIR / "organisms.json"
THRESHOLDS_FILE = DATA_DIR / "thresholds.txt"
# --- CHOOSE YOUR BLOSUM VERSION HERE ---
BLOSUM_VERSION = "blosum62"
# -----------------------------------------
SCORES_FILE = DATA_DIR / f"organisms_scores_{BLOSUM_VERSION}.json"


def load_json_data(file_path: Path) -> Dict[str, Any]:
    """Loads data from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        exit()

def load_thresholds(file_path: Path) -> List[int]:
    """Loads integer thresholds from a text file, one per line."""
    print(f"Loading thresholds from: {file_path}")
    if not file_path.exists():
        print(f"Error: Thresholds file not found at {file_path}")
        return []
    
    thresholds = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                thresholds.append(int(line))
            except (ValueError, TypeError):
                print(f"Warning: Skipping invalid line in thresholds file: '{line}'")
    return thresholds

def save_string_to_file(content: str, file_path: Path):
    """Saves a string to a file."""
    print(f"Saving file to: {file_path}")
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"Successfully saved {file_path.name}.")
    except IOError as e:
        print(f"Error: Could not write to file {file_path}. Reason: {e}")

def save_dict_to_json(data: Dict, file_path: Path):
    """Saves a dictionary to a JSON file."""
    print(f"Saving data to: {file_path}")
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Successfully saved {file_path.name}.")
    except IOError as e:
        print(f"Error: Could not write to file {file_path}. Reason: {e}")

def main():
    """
    Main pipeline to build a tree, visualize it, and extract clusters.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    organisms_data = load_json_data(ORGANISMS_FILE)
    species_names = list(organisms_data.keys())

    # Note: This assumes scores have been pre-calculated.
    # The alignment script can be run separately or integrated here if needed.
    pairwise_scores = load_json_data(SCORES_FILE)

    # --- Tree Building ---
    print("\nBuilding phylogenetic tree...")
    linkage_matrix, max_score = build_tree_from_scores(pairwise_scores, species_names)
    print("Tree construction complete.")

    # --- Newick Export ---
    newick_simple = convert_tree_to_newick(linkage_matrix, species_names, False)
    output_simple_path = OUTPUT_DIR / f"tree_{BLOSUM_VERSION}_newick.nw"
    save_string_to_file(newick_simple, output_simple_path)

    newick_with_distance = convert_tree_to_newick(linkage_matrix, species_names, True)
    output_distance_path = OUTPUT_DIR / f"tree_{BLOSUM_VERSION}_newick_with_distance.nw"
    save_string_to_file(newick_with_distance, output_distance_path)

    # --- Dendrogram Visualization ---
    dendrogram_output_path = OUTPUT_DIR / f"phylogenetic_tree_{BLOSUM_VERSION}.png"
    plot_dendrogram(linkage_matrix, species_names, dendrogram_output_path)

    # --- Cluster Extraction by Threshold ---
    print("\n--- Extracting Clusters by Threshold ---")
    thresholds = load_thresholds(THRESHOLDS_FILE)
    
    if not thresholds:
        print("No valid thresholds found. Skipping cluster extraction.")
    else:
        all_clusters_by_threshold = {}
        for threshold in sorted(thresholds, reverse=True):
            clusters = get_clusters_by_threshold(
                linkage_matrix, species_names, threshold, max_score
            )
            all_clusters_by_threshold[str(threshold)] = clusters
            
            print(f"\nClusters for threshold >= {threshold}:")
            for i, cluster in enumerate(clusters):
                print(f"  - Cluster {i+1}: {cluster}")
        
        clusters_output_path = OUTPUT_DIR / f"clusters_for_{BLOSUM_VERSION}.json"
        save_dict_to_json(all_clusters_by_threshold, clusters_output_path)

    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    main()