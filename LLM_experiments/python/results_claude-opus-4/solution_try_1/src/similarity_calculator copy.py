"""
Module for calculating pairwise similarity scores between species.
"""
from typing import Dict, Tuple
from itertools import combinations
import logging

from .sequence_alignment import NeedlemanWunsch
from .data_loader import DataLoader
from .score_saver import ScoreSaver
from .tree_builder import SingleLinkageTreeBuilder
from .tree_structures import PhylogeneticTree
from .tree_saver import TreeSaver


class SimilarityCalculator:
    """Calculates pairwise similarity scores between all species."""
    
    def __init__(self, blosum_type: int = 62):
        """
        Initialize the calculator with a specific BLOSUM matrix type.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
        """
        self.blosum_type = blosum_type
        self.logger = logging.getLogger(__name__)
        self.score_saver = ScoreSaver()
        self.tree_builder = SingleLinkageTreeBuilder()
        self.tree_saver = TreeSaver()
        
    def calculate_all_pairs(self, save_to_file: bool = True) -> Dict[Tuple[str, str], int]:
        """
        Calculate Needleman-Wunsch scores for all pairs of species.
        
        Args:
            save_to_file: Whether to save results to JSON file
            
        Returns:
            Dictionary mapping species pairs (tuple) to alignment scores
        """
        # Load data
        organisms = DataLoader.load_organisms()
        blosum_matrix = DataLoader.load_blosum_matrix(self.blosum_type)
        
        # Initialize aligner
        aligner = NeedlemanWunsch(blosum_matrix)
        
        # Calculate scores for all pairs
        scores = {}
        species_list = list(organisms.keys())
        
        self.logger.info(f"Calculating alignment scores for {len(species_list)} species")
        self.logger.info(f"Using BLOSUM{self.blosum_type} matrix")
        
        # Calculate for all unique pairs
        for species1, species2 in combinations(species_list, 2):
            seq1 = organisms[species1]
            seq2 = organisms[species2]
            
            score = aligner.align(seq1, seq2)
            
            # Store score for both orderings for fast access
            scores[(species1, species2)] = score
            scores[(species2, species1)] = score
            
            self.logger.debug(f"Score for {species1} vs {species2}: {score}")
        
        # Add self-alignment scores
        for species in species_list:
            seq = organisms[species]
            score = aligner.align(seq, seq)
            scores[(species, species)] = score
            
        self.logger.info(f"Calculated {len(scores)} pairwise alignment scores")
        
        # Save to file if requested
        if save_to_file:
            saved_path = self.score_saver.save_scores(scores, self.blosum_type)
            self.logger.info(f"Scores saved to: {saved_path}")
        
        return scores
    
    def build_phylogenetic_tree(self, scores: Dict[Tuple[str, str], int] = None) -> PhylogeneticTree:
        """
        Build a phylogenetic tree from similarity scores.
        
        Args:
            scores: Pre-calculated scores (if None, will load from file)
            
        Returns:
            PhylogeneticTree object
        """
        if scores is None:
            # Load from file
            tree = self.tree_builder.build_from_file(self.blosum_type)
        else:
            # Build from provided scores
            tree = self.tree_builder.build_tree(scores)
        
        return tree
    
    def save_tree_newick(self, tree: PhylogeneticTree) -> Tuple[str, str]:
        """
        Save tree in both Newick format variants.
        
        Args:
            tree: PhylogeneticTree to save
            
        Returns:
            Tuple of (simple_newick_path, distance_newick_path)
        """
        return self.tree_saver.save_newick_formats(tree, self.blosum_type)