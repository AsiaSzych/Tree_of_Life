"""
Main entry point for the phylogenetic clustering project.
"""
import sys
from pathlib import Path
from src.alignment import (
    calculate_all_pairwise_scores, 
    load_organisms,
    save_scores_to_json
)
from src.tree import (
    build_phylogenetic_tree, 
    save_tree_to_newick,
    extract_blosum_version_from_scores_file
)
from src.tree.tree_utils import get_tree_statistics, validate_tree_structure
from src.visualization import save_dendrogram
from src.clustering.threshold_clustering import run_threshold_clustering
from src.clustering.cluster_visualization import plot_cluster_size_distribution


def run_complete_analysis(organisms_file: str, blosum_file: str):
    """
    Run the complete phylogenetic analysis pipeline.
    
    Args:
        organisms_file: Path to organisms JSON file
        blosum_file: Path to BLOSUM scoring matrix file
    """
    # Extract BLOSUM version
    blosum_version = Path(blosum_file).stem
    
    # Step 1: Calculate alignment scores
    print("="*60)
    print(f"Step 1: Calculating alignment scores using {blosum_file}...")
    print("="*60)
    
    organisms = load_organisms(organisms_file)
    print(f"Loaded {len(organisms)} organisms")
    
    pairwise_scores = calculate_all_pairwise_scores(organisms, blosum_file)
    scores_file = save_scores_to_json(pairwise_scores, blosum_file)
    
    # Step 2: Build phylogenetic tree
    print("\n" + "="*60)
    print("Step 2: Building phylogenetic tree...")
    print("="*60)
    
    tree = build_phylogenetic_tree(scores_file)
    
    # Validate tree
    is_valid, errors = validate_tree_structure(tree)
    if not is_valid:
        print("Tree validation errors:")
        for error in errors:
            print(f"  - {error}")
        return
    
    # Get statistics
    stats = get_tree_statistics(tree)
    print("\nTree Statistics:")
    print(f"  Number of species: {stats['num_species']}")
    print(f"  Tree depth: {stats['tree_depth']}")
    print(f"  Score range: {stats['min_merge_height']} - {stats['max_merge_height']}")
    
    # Save tree to Newick formats
    save_tree_to_newick(tree, blosum_version)
    
    # Step 3: Create dendrogram
    print("\n" + "="*60)
    print("Step 3: Creating dendrogram visualization...")
    print("="*60)
    
    save_dendrogram(tree, blosum_version)
    
    # Step 4: Threshold-based clustering
    print("\n" + "="*60)
    print("Step 4: Performing threshold-based clustering...")
    print("="*60)
    
    thresholds_file = "thresholds.txt"
    if Path(thresholds_file).exists():
        clusters_by_threshold = run_threshold_clustering(
            tree, thresholds_file, blosum_version
        )
        
        # Create cluster analysis plot
        plot_cluster_size_distribution(clusters_by_threshold, blosum_version)
    else:
        print(f"Warning: {thresholds_file} not found. Skipping clustering step.")
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)


def main():
    """Main function to run the alignment calculations."""
    # Default configuration
    organisms_file = "organisms.json"
    blosum_file = "blosum62.json"  # Default to blosum62
    
    # Check if BLOSUM file is specified as command line argument
    if len(sys.argv) > 1:
        blosum_arg = sys.argv[1]
        if blosum_arg in ["blosum50.json", "blosum62.json"]:
            blosum_file = blosum_arg
        else:
            print(f"Warning: Invalid BLOSUM file '{blosum_arg}'. Using default: {blosum_file}")
    
    try:
        # Check required files
        required_files = [organisms_file, blosum_file]
        missing_files = [f for f in required_files if not Path(f).exists()]
        
        if missing_files:
            print("Error: Missing required files:")
            for f in missing_files:
                print(f"  - {f}")
            return
        
        # Run the complete analysis
        run_complete_analysis(organisms_file, blosum_file)
        
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()