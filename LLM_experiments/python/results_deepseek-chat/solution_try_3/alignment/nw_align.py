"""Implementation of Needleman-Wunsch global alignment algorithm."""

from typing import Tuple, Dict
from .scoring import get_substitution_score, get_deletion_score

def needleman_wunsch(
    seq1: str, 
    seq2: str, 
    blosum: Dict[str, int]
) -> int:
    """Calculate Needleman-Wunsch alignment score.
    
    Args:
        seq1: First sequence to align
        seq2: Second sequence to align
        blosum: BLOSUM substitution matrix
        
    Returns:
        Alignment score (integer)
    """
    m, n = len(seq1), len(seq2)
    
    # Initialize DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill first row and column with gap penalties
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + get_deletion_score(blosum, seq1[i-1])
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + get_deletion_score(blosum, seq2[j-1])
    
    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + get_substitution_score(
                blosum, seq1[i-1], seq2[j-1]
            )
            delete_in_seq1 = dp[i-1][j] + get_deletion_score(blosum, seq1[i-1])
            delete_in_seq2 = dp[i][j-1] + get_deletion_score(blosum, seq2[j-1])
            dp[i][j] = max(match, delete_in_seq1, delete_in_seq2)
    
    return dp[m][n]