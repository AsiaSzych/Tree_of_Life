import json
from pathlib import Path
from typing import Dict

def save_newick_files(tree_root, blosum_type: str, output_dir: str = "./output"):
    """
    Save two versions of Newick format tree to files.
    
    Args:
        tree_root: Root node of the phylogenetic tree
        blosum_type: BLOSUM matrix version (50 or 62)
        output_dir: Directory to save files (default: ./output)
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Simple Newick (no distances)
    simple_path = Path(output_dir) / f"tree_blosum{blosum_type}_newick.nw"
    with open(simple_path, 'w') as f:
        f.write(tree_root.get_simple_newick() + ";")
    
    # Newick with distances
    dist_path = Path(output_dir) / f"tree_blosum{blosum_type}_newick_with_distance.nw"
    with open(dist_path, 'w') as f:
        f.write(tree_root.get_newick_with_distances() + ";")