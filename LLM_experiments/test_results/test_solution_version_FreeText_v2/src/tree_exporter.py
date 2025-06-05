# src/tree_exporter.py
import os
import re
import numpy as np
from typing import List, Tuple

from Bio import Phylo # Import Biopython's Phylo module

class TreeExporter:
    """
    A class to export phylogenetic trees to Newick format from scipy linkage matrices.
    """

    def __init__(self, output_dir: str):
        """
        Initializes the TreeExporter.

        Args:
            output_dir (str): The directory where the Newick files should be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True) # Ensure output directory exists

    def export_to_newick(
        self,
        linkage_matrix: np.ndarray,
        species_labels: List[str],
        blosum_matrix_filepath: str
    ) -> Tuple[str, str]:
        """
        Exports the phylogenetic tree to two Newick formats:
        1. With only node names.
        2. With node names and branch lengths (distances).

        Args:
            linkage_matrix (np.ndarray): The hierarchical clustering linkage matrix (Z).
            species_labels (List[str]): The ordered list of original species labels.
            blosum_matrix_filepath (str): The path to the BLOSUM matrix file used,
                                          to determine the output filename.

        Returns:
            Tuple[str, str]: A tuple containing the file paths of the saved Newick files:
                             (filepath_no_distances, filepath_with_distances).
        """
        # Extract BLOSUM version from the filename
        match = re.search(r'blosum(\d+)\.json$', blosum_matrix_filepath)
        if not match:
            raise ValueError(
                f"Could not extract BLOSUM version from filename: {blosum_matrix_filepath}. "
                "Expected format like 'blosumXX.json'."
            )
        blosum_version = match.group(1)

        # 1. Create tree with distances (branch lengths)
        # Bio.Phylo.from_linkage directly uses the distances from the linkage matrix
        # as branch lengths.
        tree_with_distances = Phylo.from_linkage(linkage_matrix, species_labels)
        filepath_with_distances = os.path.join(
            self.output_dir, f"tree{blosum_version}_newick_with_distance.nw"
        )
        Phylo.write(tree_with_distances, filepath_with_distances, "newick")
        print(f"Tree with distances saved to: '{filepath_with_distances}'")

        # 2. Create tree without distances (by setting branch_length to None)
        # We need to create a copy or re-generate the tree to modify it
        tree_no_distances = Phylo.from_linkage(linkage_matrix, species_labels)
        for clade in tree_no_distances.find_clades():
            clade.branch_length = None # Set branch length to None to omit it in Newick output

        filepath_no_distances = os.path.join(
            self.output_dir, f"tree{blosum_version}_newick.nw"
        )
        Phylo.write(tree_no_distances, filepath_no_distances, "newick")
        print(f"Tree without distances saved to: '{filepath_no_distances}'")

        return filepath_no_distances, filepath_with_distances
