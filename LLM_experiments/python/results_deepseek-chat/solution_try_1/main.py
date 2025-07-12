from alignment.io import load_organisms, load_thresholds, save_scores
from alignment.nw import compute_all_pairs
from alignment.tree import PhylogeneticTree
import json
import re

def get_blosum_type(blosum_path: str) -> str:
    """Extract BLOSUM version from filename."""
    match = re.search(r'blosum(\d+)\.json$', blosum_path)
    if not match:
        raise ValueError("Invalid BLOSUM filename format")
    return match.group(1)

def main():
    # Load data
    organisms = load_organisms('./data/organisms.json')
    blosum_file = './data/blosum62.json'  # Default to BLOSUM62
    blosum_type = get_blosum_type(blosum_file)
    
    # Compute scores and build tree
    scores = compute_all_pairs(organisms, blosum_file)
    save_scores(scores, blosum_type)
    
    tree = PhylogeneticTree(scores)
    tree.build_tree()
    tree.plot_dendrogram(blosum_type)
    
    # Simple Newick (no distances)
    with open(f'./tree_blosum{blosum_type}_newick.nw', 'w') as f:
        f.write(tree.get_simple_newick() + ';')
    
    # Newick with distances (integer values)
    with open(f'./tree_blosum{blosum_type}_newick_with_distance.nw', 'w') as f:
        f.write(tree.get_distance_newick() + ';')
    
    print(f"Saved Newick formats:")
    print(f"- Simple: tree_blosum{blosum_type}_newick.nw")
    print(f"- With distances: tree_blosum{blosum_type}_newick_with_distance.nw")

    # Process thresholds
    thresholds = load_thresholds('./data/thresholds.txt')
    clusters = {
        t: tree.get_clusters_at_threshold(t)
        for t in thresholds
    }
    
    # Save and print results
    with open(f'./outputs/clusters_for_blosum{blosum_type}.json', 'w') as f:
        json.dump(clusters, f, indent=2)
    
    print("Cluster Results:")
    for threshold, cluster_list in sorted(clusters.items()):
        print(f"\nThreshold: {threshold}")
        for i, cluster in enumerate(cluster_list, 1):
            print(f"Cluster {i}: {', '.join(cluster)}")

if __name__ == '__main__':
    main()