"""Implementation of the Needleman-Wunsch algorithm for sequence alignment."""

import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class NeedlemanWunsch:
    """Needleman-Wunsch algorithm for global sequence alignment."""
    
    def __init__(self, blosum_matrix: Dict[str, int]):
        """
        Initialize with BLOSUM substitution matrix.
        
        Args:
            blosum_matrix: Dictionary containing gap penalties and substitution scores
        """
        self.blosum_matrix = blosum_matrix
        self._validate_matrix()
    
    def _validate_matrix(self) -> None:
        """Validate that the BLOSUM matrix contains necessary entries."""
        # Check for at least some single character (gap) entries
        has_gaps = any(len(k) == 1 for k in self.blosum_matrix.keys())
        # Check for at least some substitution entries
        has_substitutions = any(len(k) == 2 for k in self.blosum_matrix.keys())
        
        if not has_gaps or not has_substitutions:
            raise ValueError("BLOSUM matrix must contain both gap and substitution scores")
    
    def _get_gap_penalty(self, amino_acid: str) -> int:
        """
        Get gap penalty for a specific amino acid.
        
        Args:
            amino_acid: Single character amino acid
            
        Returns:
            Gap penalty (typically negative)
        """
        return self.blosum_matrix.get(amino_acid.lower(), -1)
    
    def _get_substitution_score(self, aa1: str, aa2: str) -> int:
        """
        Get substitution score between two amino acids.
        
        Args:
            aa1: First amino acid
            aa2: Second amino acid
            
        Returns:
            Substitution score
        """
        # Try both possible key orders
        # key1 = f"{aa1.lower()}{aa2.lower()}"
        # key2 = f"{aa2.lower()}{aa1.lower()}"
        key1 = f"{aa1}{aa2}"
        key2 = f"{aa2}{aa1}"
        if key1 in self.blosum_matrix:
            return self.blosum_matrix[key1]
        elif key2 in self.blosum_matrix:
            return self.blosum_matrix[key2]
        else:
            # Default penalty if not found
            logger.warning(f"Substitution score not found for {aa1}-{aa2}, using default -1")
            return -1
    
    def align(self, seq1: str, seq2: str) -> int:
        """
        Calculate Needleman-Wunsch alignment score for two sequences.
        
        Args:
            seq1: First amino acid sequence
            seq2: Second amino acid sequence
            
        Returns:
            Alignment score (integer)
        """
        if not seq1 or not seq2:
            return 0
        
        m, n = len(seq1), len(seq2)
        
        # Initialize scoring matrix
        score_matrix = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        # Initialize first row and column with gap penalties
        for i in range(1, m + 1):
            score_matrix[i][0] = score_matrix[i-1][0] + self._get_gap_penalty(seq1[i-1])
        
        for j in range(1, n + 1):
            score_matrix[0][j] = score_matrix[0][j-1] + self._get_gap_penalty(seq2[j-1])
        
        # Fill the scoring matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Match/mismatch score
                match_score = score_matrix[i-1][j-1] + self._get_substitution_score(
                    seq1[i-1], seq2[j-1]
                )
                
                # Gap in sequence 2
                gap1_score = score_matrix[i-1][j] + self._get_gap_penalty(seq1[i-1])
                
                # Gap in sequence 1
                gap2_score = score_matrix[i][j-1] + self._get_gap_penalty(seq2[j-1])
                
                # Take maximum score
                score_matrix[i][j] = max(match_score, gap1_score, gap2_score)
        
        # Return the final alignment score
        return score_matrix[m][n]