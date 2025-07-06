import json
import sys
import os
from typing import Dict, List
from blosum_loader import BlosumLoader
from nw_aligner import needleman_wunsch
from similarity_matrix import SimilarityMatrix
from tree_builder import TreeBuilder
from tree_node import TreeNode
from tree_serializer import TreeSerializer
from dendrogram_visualizer import DendrogramVisualizer
from cluster_extractor import ClusterExtractor

def save_scores_to_json(scores: Dict[str, int], blosum_filename: str):
    matrix_type = blosum_filename.replace("blosum", "").replace(".json", "")
    output_filename = f"./organisms_scores_blosum{matrix_type}.json"
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    with open(output_filename, 'w') as f:
        json.dump(scores, f, indent=4)
    print(f"Saved scores to {output_filename}")

def save_newick_files(tree: TreeNode, blosum_filename: str):
    matrix_type = blosum_filename.replace("blosum", "").replace(".json", "")
    simple_nw = TreeSerializer.to_simple_newick(tree) + ";"
    distance_nw = TreeSerializer.to_distance_newick(tree) + ";"
    
    simple_filename = f"./tree_blosum{matrix_type}_newick.nw"
    with open(simple_filename, 'w') as f: f.write(simple_nw)
    
    distance_filename = f"./tree_blosum{matrix_type}_newick_with_distance.nw"
    with open(distance_filename, 'w') as f: f.write(distance_nw)
    print(f"Saved Newick files: {simple_filename}, {distance_filename}")

def save_dendrogram(tree: TreeNode, blosum_filename: str):
    matrix_type = blosum_filename.replace("blosum", "").replace(".json", "")
    output_filename = f"./phylogenetic_tree_blosum{matrix_type}.png"
    visualizer = DendrogramVisualizer()
    visualizer.plot(tree, output_filename)

def process_thresholds(tree: TreeNode, blosum_filename: str):
    matrix_type = blosum_filename.replace("blosum", "").replace(".json", "")
    output_filename = f"./clusters_for_blosum{matrix_type}.json"
    
    try:
        with open("./thresholds.txt", "r") as f:
            thresholds = [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: thresholds.txt file not found")
        return
    except ValueError:
        print("Error: thresholds.txt contains non-integer values")
        return
    
    if not thresholds:
        print("Warning: thresholds.txt is empty")
        return
    
    clusters_dict = {}
    for threshold in thresholds:
        clusters = ClusterExtractor.extract_clusters(tree, threshold)
        clusters_dict[threshold] = clusters
        print(f"\nThreshold: {threshold}\nClusters: {len(clusters)}")
        for i, cluster in enumerate(clusters, 1):
            print(f"  Cluster {i}: {', '.join(cluster)}")
    
    with open(output_filename, "w") as f:
        json.dump(clusters_dict, f, indent=4)
    print(f"\nSaved clusters to {output_filename}")

def main(blosum_file: str):
    with open('./organisms.json', 'r') as f:
        organisms = json.load(f)
    
    blosum = BlosumLoader(f'./{blosum_file}')
    species = list(organisms.keys())
    similarity_matrix = SimilarityMatrix(species)
    scores_dict = {}
    
    species_list = list(species)
    for i in range(len(species_list)):
        for j in range(i + 1, len(species_list)):
            species1 = species_list[i]
            species2 = species_list[j]
            score = needleman_wunsch(
                organisms[species1],
                organisms[species2],
                blosum
            )
            similarity_matrix.add_score(species1, species2, score)
            scores_dict[f"{species1}_{species2}"] = int(score)
    
    save_scores_to_json(scores_dict, blosum_file)
    
    tree_builder = TreeBuilder(similarity_matrix, species_list)
    phylogenetic_tree = tree_builder.build_tree()
    print("\nPhylogenetic tree constructed successfully!")
    
    save_newick_files(phylogenetic_tree, blosum_file)
    save_dendrogram(phylogenetic_tree, blosum_file)
    process_thresholds(phylogenetic_tree, blosum_file)
    
    test_blosum = BlosumLoader(f'./{blosum_file}')
    test_score = needleman_wunsch("aabaab", "ababaa", test_blosum)
    print(f"\nTest alignment score: {test_score} (Expected: 7)")
    return similarity_matrix, phylogenetic_tree

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <blosum_file>")
        sys.exit(1)
    similarity_matrix, tree = main(sys.argv[1])