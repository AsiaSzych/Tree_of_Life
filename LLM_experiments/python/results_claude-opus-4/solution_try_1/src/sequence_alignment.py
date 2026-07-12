"""
Module for Needleman-Wunsch sequence alignment algorithm implementation.
"""
from typing import Dict, Tuple
import numpy as np


class NeedlemanWunsch:
    """Implements the Needleman-Wunsch algorithm for global sequence alignment."""
    
    def __init__(self, blosum_matrix: Dict[str, int]):
        """
        Initialize the aligner with a BLOSUM substitution matrix.
        
        Args:
            blosum_matrix: Dictionary with gap penalties (single char keys) 
                          and substitution scores (two char keys)
        """
        self.blosum_matrix = blosum_matrix
    
    def _get_gap_penalty(self, amino_acid: str) -> int:
        """Get the gap penalty for a specific amino acid."""
        return self.blosum_matrix.get(amino_acid, 0)
    
    def _get_substitution_score(self, aa1: str, aa2: str) -> int:
        """Get the substitution score between two amino acids."""
        key = aa1 + aa2
        return self.blosum_matrix.get(key, 0)
    
    def align(self, seq1: str, seq2: str) -> int:
        """
        Perform Needleman-Wunsch alignment between two sequences.
        
        Args:
            seq1: First amino acid sequence
            seq2: Second amino acid sequence
            
        Returns:
            Alignment score (integer)
        """
        m, n = len(seq1), len(seq2)
        
        # Initialize the scoring matrix
        score_matrix = np.zeros((m + 1, n + 1), dtype=int)
        
        # Initialize first row (gaps in seq1)
        for j in range(1, n + 1):
            score_matrix[0][j] = score_matrix[0][j-1] + self._get_gap_penalty(seq2[j-1])
        
        # Initialize first column (gaps in seq2)
        for i in range(1, m + 1):
            score_matrix[i][0] = score_matrix[i-1][0] + self._get_gap_penalty(seq1[i-1])
        
        # Fill the scoring matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Match/mismatch score
                match_score = score_matrix[i-1][j-1] + self._get_substitution_score(seq1[i-1], seq2[j-1])
                
                # Gap in seq2 (deletion from seq1)
                gap_seq2 = score_matrix[i-1][j] + self._get_gap_penalty(seq1[i-1])
                
                # Gap in seq1 (deletion from seq2)
                gap_seq1 = score_matrix[i][j-1] + self._get_gap_penalty(seq2[j-1])
                
                # Take maximum score
                score_matrix[i][j] = max(match_score, gap_seq2, gap_seq1)
        
        return int(score_matrix[m][n])