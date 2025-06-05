# filename: main.py
import json
import itertools
import argparse
from pathlib import Path
from typing import Dict, Any, FrozenSet, List

from alignment import needleman_wunsch
from clustering import build_tree, tree_to_newick, get_clusters_at_threshold
from visualization import draw_dendrogram

def load_json_data(file_path: Path) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as f: return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Fatal Error: Could not read or parse {file_path}. Reason: {e}"); exit(1)

def load_thresholds(file_path: Path) -> List[float]:
    try:
        with open(file_path, 'r') as f: return [float(line.strip()) for line in f if line.strip()]
    except (FileNotFoundError, ValueError) as e:
        print(f"Fatal Error: Could not read or parse {file_path}. Reason: {e}"); exit(1)

def save_output_file(data: Any, file_path: Path):
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w') as f:
            if isinstance(data, dict): json.dump(data, f, indent=4)
            else: f.write(str(data))
        print(f"Successfully saved output to {file_path}")
    except IOError as e: print(f"Error: Could not write to {file_path}. Reason: {e}")

def calculate_all_scores(organisms: Dict[str, str], scores: Dict[str, int]) -> Dict[FrozenSet[str], int]:
    species_names = list(organisms.keys())
    similarity_scores = {}
    print(f"Calculating {len(species_names) * (len(species_names) - 1) // 2} pairwise scores...")
    for s1, s2 in itertools.combinations(species_names, 2):
        score = needleman_wunsch(organisms[s1], organisms[s2], scores)
        similarity_scores[frozenset({s1, s2})] = score
    return similarity_scores

def format_scores_for_saving(scores: Dict[FrozenSet[str], int]) -> Dict[str, int]:
    return {f"{s1}_{s2}": int(score) for (s1, s2), score in [(sorted(list(pair)), score) for pair, score in scores.items()]}

def main():
    parser = argparse.ArgumentParser(description="A complete phylogenetic analysis pipeline.")
    parser.add_argument("--organisms_file", type=str, default="organisms.json", help="Organisms JSON file in 'data' folder.")
    parser.add_argument("--blosum_file", type=str, default="blosum50.json", help="BLOSUM JSON file in 'data' folder.")
    parser.add_argument("--threshold_file", type=str, default="thresholds.txt", help="Thresholds text file in 'data' folder.")
    args = parser.parse_args()

    print("--- Phase 1: Setup and Data Loading ---")
    data_dir, output_dir = Path("data"), Path("output")
    organisms = load_json_data(data_dir / args.organisms_file)
    blosum_scores = load_json_data(data_dir / args.blosum_file)
    thresholds = load_thresholds(data_dir / args.threshold_file)
    print("All input files loaded successfully.\n")

    print("--- Phase 2: Pairwise Score Calculation ---")
    similarity_scores = calculate_all_scores(organisms, blosum_scores)
    file_base_name = Path(args.blosum_file).stem
    scores_to_save = format_scores_for_saving(similarity_scores)
    save_output_file(scores_to_save, output_dir / f"organisms_scores_{file_base_name}.json")
    print("Pairwise scores calculated and saved.\n")

    print("--- Phase 3: Tree Construction and Visualization ---")
    root_node = build_tree(similarity_scores)
    if not root_node: print("Fatal Error: Could not build tree. Exiting."); return
    all_species = sorted(list(organisms.keys()))
    save_output_file(tree_to_newick(root_node, False), output_dir / f"tree_{file_base_name}_newick.nw")
    save_output_file(tree_to_newick(root_node, True), output_dir / f"tree_{file_base_name}_newick_with_distance.nw")
    draw_dendrogram(root_node, all_species, output_dir / f"phylogenetic_tree_{file_base_name}.png")
    print("Tree representations created and saved.\n")

    print("--- Phase 4: Cluster Extraction ---")
    all_cluster_results = {}
    for threshold in thresholds:
        clusters = get_clusters_at_threshold(root_node, threshold)
        all_cluster_results[str(threshold)] = clusters
        print(f"\nClusters for Threshold: {threshold}")
        for i, cluster in enumerate(clusters): print(f"  - Cluster {i+1}: {cluster}")
    save_output_file(all_cluster_results, output_dir / f"clusters_for_{file_base_name}.json")
    print("\n--- Pipeline Finished Successfully ---")

if __name__ == "__main__":
    main()