"""
Needleman-Wunsch algorithm implementation for global sequence alignment.
"""
import json
from typing import Dict, Tuple, List
import numpy as np
from pathlib import Path


class NeedlemanWunsch:
    """
    Implementation of Needleman-Wunsch algorithm for global sequence alignment.
    """
    
    def __init__(self, blosum_file: str):
        """
        Initialize the Needleman-Wunsch algorithm with a BLOSUM scoring matrix.
        
        Args:
            blosum_file: Path to the BLOSUM JSON file (e.g., 'blosum50.json')
        """
        self.blosum_file = blosum_file
        self.scoring_matrix = self._load_blosum_matrix()
    
    def _load_blosum_matrix(self) -> Dict[str, int]:
        """
        Load BLOSUM scoring matrix from JSON file.
        
        Returns:
            Dictionary with scoring values
        """
        file_path = Path(self.blosum_file)
        if not file_path.exists():
            raise FileNotFoundError(f"BLOSUM file not found: {self.blosum_file}")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _get_gap_penalty(self, amino_acid: str) -> int:
        """
        Get gap penalty for a specific amino acid.
        
        Args:
            amino_acid: Single character amino acid
            
        Returns:
            Gap penalty (negative value)
        """
        return self.scoring_matrix.get(amino_acid.lower(), -1)
    
    def _get_substitution_score(self, aa1: str, aa2: str) -> int:
        """
        Get substitution score between two amino acids.
        
        Args:
            aa1: First amino acid
            aa2: Second amino acid
            
        Returns:
            Substitution score
        """
        key = f"{aa1.lower()}{aa2.lower()}"
        return self.scoring_matrix.get(key, -1)
    
    def align(self, seq1: str, seq2: str) -> int:
        """
        Perform Needleman-Wunsch alignment and return the alignment score.
        
        Args:
            seq1: First amino acid sequence
            seq2: Second amino acid sequence
            
        Returns:
            Alignment score (integer)
        """
        # Initialize dimensions
        m, n = len(seq1), len(seq2)
        
        # Initialize scoring matrix with zeros
        score_matrix = np.zeros((m + 1, n + 1), dtype=int)
        
        # Initialize first column (gaps in seq2)
        for i in range(1, m + 1):
            score_matrix[i, 0] = score_matrix[i-1, 0] + self._get_gap_penalty(seq1[i-1])
        
        # Initialize first row (gaps in seq1)
        for j in range(1, n + 1):
            score_matrix[0, j] = score_matrix[0, j-1] + self._get_gap_penalty(seq2[j-1])
        
        # Fill the scoring matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Match/mismatch score
                match_score = score_matrix[i-1, j-1] + self._get_substitution_score(
                    seq1[i-1], seq2[j-1]
                )
                
                # Gap in seq2
                gap1_score = score_matrix[i-1, j] + self._get_gap_penalty(seq1[i-1])
                
                # Gap in seq1
                gap2_score = score_matrix[i, j-1] + self._get_gap_penalty(seq2[j-1])
                
                # Take maximum score
                score_matrix[i, j] = max(match_score, gap1_score, gap2_score)
        
        # Return the final alignment score
        return int(score_matrix[m, n])


def load_organisms(filename: str = "organisms.json") -> Dict[str, str]:
    """
    Load organism sequences from JSON file.
    
    Args:
        filename: Path to organisms JSON file
        
    Returns:
        Dictionary mapping species names to sequences
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"Organisms file not found: {filename}")
    
    with open(file_path, 'r') as f:
        return json.load(f)


def calculate_all_pairwise_scores(
    organisms: Dict[str, str], 
    blosum_file: str
) -> Dict[Tuple[str, str], int]:
    """
    Calculate Needleman-Wunsch scores for all pairs of organisms.
    
    Args:
        organisms: Dictionary mapping species names to sequences
        blosum_file: Path to BLOSUM scoring matrix file
        
    Returns:
        Dictionary mapping species pairs to alignment scores
    """
    # Initialize aligner
    aligner = NeedlemanWunsch(blosum_file)
    
    # Get all species names
    species_list = list(organisms.keys())
    n_species = len(species_list)
    
    # Calculate scores for all pairs
    pairwise_scores = {}
    
    for i in range(n_species):
        for j in range(i + 1, n_species):
            species1 = species_list[i]
            species2 = species_list[j]
            
            seq1 = organisms[species1]
            seq2 = organisms[species2]
            
            # Calculate alignment score
            score = aligner.align(seq1, seq2)
            
            # Store score for both directions (symmetric)
            pairwise_scores[(species1, species2)] = score
            pairwise_scores[(species2, species1)] = score
    
    # Add self-alignment scores
    for species in species_list:
        seq = organisms[species]
        score = aligner.align(seq, seq)
        pairwise_scores[(species, species)] = score
    
    return pairwise_scores