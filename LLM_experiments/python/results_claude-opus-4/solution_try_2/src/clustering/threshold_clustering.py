"""
Module for threshold-based clustering of species from phylogenetic trees.
"""
import json
from pathlib import Path
from typing import List, Dict
from src.tree.phylogenetic_tree import PhylogeneticTree


def load_thresholds(filename: str = "thresholds.txt") -> List[int]:
    """
    Load threshold values from text file.
    
    Args:
        filename: Path to thresholds file
        
    Returns:
        List of integer threshold values
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"Thresholds file not found: {filename}")
    
    thresholds = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                try:
                    threshold = int(line)
                    thresholds.append(threshold)
                except ValueError:
                    print(f"Warning: Skipping invalid threshold value: {line}")
    
    return sorted(thresholds, reverse=True)  # Sort from highest to lowest


def calculate_clusters_for_thresholds(
    tree: PhylogeneticTree, 
    thresholds: List[int]
) -> Dict[int, List[List[str]]]:
    """
    Calculate clusters for multiple threshold values.
    
    Args:
        tree: PhylogeneticTree object
        thresholds: List of threshold values
        
    Returns:
        Dictionary mapping thresholds to cluster lists
    """
    clusters_by_threshold = {}
    
    for threshold in thresholds:
        # Get clusters at this threshold
        clusters = tree.get_clusters_at_threshold(threshold)
        
        # Sort clusters by size (largest first) and then alphabetically
        clusters_sorted = sorted(
            clusters, 
            key=lambda c: (-len(c), sorted(c)[0])
        )
        
        # Sort species within each cluster alphabetically
        clusters_sorted = [sorted(cluster) for cluster in clusters_sorted]
        
        clusters_by_threshold[threshold] = clusters_sorted
        
        # Print results
        print(f"\nThreshold: {threshold}")
        print(f"Number of clusters: {len(clusters_sorted)}")
        for i, cluster in enumerate(clusters_sorted, 1):
            print(f"  Cluster {i} ({len(cluster)} species): {', '.join(cluster)}")
    
    return clusters_by_threshold


def save_clusters_to_json(
    clusters_by_threshold: Dict[int, List[List[str]]],
    blosum_version: str,
    output_dir: str = "."
) -> str:
    """
    Save clustering results to JSON file.
    
    Args:
        clusters_by_threshold: Dictionary mapping thresholds to clusters
        blosum_version: BLOSUM version used (e.g., "blosum50", "blosum62")
        output_dir: Directory to save output file
        
    Returns:
        Path to saved file
    """
    # Create output directory if needed
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate filename
    filename = output_path / f"clusters_for_{blosum_version}.json"
    
    # Save to JSON
    with open(filename, 'w') as f:
        json.dump(clusters_by_threshold, f, indent=2)
    
    print(f"\nClusters saved to: {filename}")
    return str(filename)


def analyze_clustering_results(
    clusters_by_threshold: Dict[int, List[List[str]]]
) -> Dict[str, any]:
    """
    Analyze clustering results to provide statistics.
    
    Args:
        clusters_by_threshold: Dictionary mapping thresholds to clusters
        
    Returns:
        Dictionary with clustering statistics
    """
    stats = {}
    
    for threshold, clusters in clusters_by_threshold.items():
        cluster_sizes = [len(cluster) for cluster in clusters]
        
        stats[threshold] = {
            "num_clusters": len(clusters),
            "min_cluster_size": min(cluster_sizes) if cluster_sizes else 0,
            "max_cluster_size": max(cluster_sizes) if cluster_sizes else 0,
            "avg_cluster_size": sum(cluster_sizes) / len(cluster_sizes) if cluster_sizes else 0,
            "singleton_clusters": sum(1 for size in cluster_sizes if size == 1)
        }
    
    return stats


def run_threshold_clustering(
    tree: PhylogeneticTree,
    thresholds_file: str,
    blosum_version: str,
    output_dir: str = "."
) -> Dict[int, List[List[str]]]:
    """
    Complete threshold clustering workflow.
    
    Args:
        tree: PhylogeneticTree object
        thresholds_file: Path to thresholds file
        blosum_version: BLOSUM version used
        output_dir: Directory for output files
        
    Returns:
        Dictionary mapping thresholds to clusters
    """
    # Load thresholds
    print(f"Loading thresholds from {thresholds_file}...")
    thresholds = load_thresholds(thresholds_file)
    print(f"Loaded {len(thresholds)} threshold values: {thresholds}")
    
    # Calculate clusters
    print("\nCalculating clusters for each threshold...")
    clusters_by_threshold = calculate_clusters_for_thresholds(tree, thresholds)
    
    # Save results
    save_clusters_to_json(clusters_by_threshold, blosum_version, output_dir)
    
    # Print statistics
    print("\nClustering Statistics:")
    stats = analyze_clustering_results(clusters_by_threshold)
    for threshold in sorted(stats.keys(), reverse=True):
        s = stats[threshold]
        print(f"  Threshold {threshold}: {s['num_clusters']} clusters, "
              f"sizes {s['min_cluster_size']}-{s['max_cluster_size']} "
              f"(avg: {s['avg_cluster_size']:.1f}), "
              f"{s['singleton_clusters']} singletons")
    
    return clusters_by_threshold