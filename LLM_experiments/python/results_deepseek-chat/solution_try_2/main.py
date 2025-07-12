import sys
import json
from pathlib import Path
from io_handler.file_reader import read_organisms, read_blosum_matrix, save_scores_to_json
from io_handler.newick_writer import save_newick_files
from alignment.scoring import BlosumScorer
from alignment.nw import calculate_all_pairs
from tree.builder import TreeBuilder
from visualization.dendrogram import plot_dendrogram
from clustering.threshold import read_thresholds, get_clusters_at_threshold, save_clusters_to_json

def main(organisms_path: str, blosum_path: str, thresholds_path: str) -> None:
    try:
        # Existing pipeline
        organisms = read_organisms(organisms_path)
        blosum_data = read_blosum_matrix(blosum_path)
        blosum_type = Path(blosum_path).stem.replace("blosum", "")
        scorer = BlosumScorer(blosum_data)
        scores = calculate_all_pairs(organisms, scorer)
        save_scores_to_json(scores, blosum_type)
        
        # Build tree
        tree_builder = TreeBuilder(scores)
        phylogenetic_tree = tree_builder.build_tree()
        
        # Save outputs
        save_newick_files(phylogenetic_tree, blosum_type)
        plot_dendrogram(phylogenetic_tree, blosum_type)
        
        # Process thresholds
        thresholds = read_thresholds(thresholds_path)
        clusters = {}
        
        print("\nCluster Results:")
        for threshold in thresholds:
            current_clusters = get_clusters_at_threshold(phylogenetic_tree, threshold)
            clusters[threshold] = current_clusters
            
            print(f"\nThreshold: {threshold}")
            for i, cluster in enumerate(current_clusters, 1):
                print(f"Cluster {i}: {', '.join(cluster)}")
        
        # Save clusters to JSON
        save_clusters_to_json(clusters, blosum_type)
        print(f"\nSaved clusters to ./output/clusters_for_blosum{blosum_type}.json")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py organisms.json blosumXX.json thresholds.txt")
        sys.exit(1)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3])