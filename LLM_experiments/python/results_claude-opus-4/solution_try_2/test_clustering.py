"""
Test script for clustering functionality.
"""
from pathlib import Path
import json
from src.tree import build_phylogenetic_tree
from src.clustering import run_threshold_clustering


def create_test_thresholds():
    """Create a test thresholds file."""
    # Create test thresholds
    thresholds = [1260, 1150, 980, 850, 700]
    
    with open("test_thresholds.txt", 'w') as f:
        for t in thresholds:
            f.write(f"{t}\n")
    
    print(f"Created test thresholds file with values: {thresholds}")


def test_clustering():
    """Test the clustering functionality."""
    # Check if we have a scores file
    scores_files = list(Path(".").glob("organisms_scores_blosum*.json"))
    
    if not scores_files:
        print("No scores files found. Run the main analysis first.")
        return
    
    scores_file = scores_files[0]
    print(f"Using scores file: {scores_file}")
    
    # Extract blosum version
    blosum_version = scores_file.stem.split('_')[-1]
    
    # Create test thresholds if needed
    if not Path("test_thresholds.txt").exists():
        create_test_thresholds()
    
    # Build tree
    print("\nBuilding tree...")
    tree = build_phylogenetic_tree(str(scores_file))
    
    # Run clustering
    print("\nRunning clustering...")
    run_threshold_clustering(tree, "test_thresholds.txt", blosum_version)


if __name__ == "__main__":
    test_clustering()