import numpy as np
from typing import Dict, Tuple
from .scoring import BlosumScorer
from .io import load_blosum_matrix

def needleman_wunsch(seq1: str, seq2: str, scorer: BlosumScorer) -> int:
    """Compute Needleman-Wunsch alignment score."""
    m, n = len(seq1), len(seq2)
    dp = np.zeros((m + 1, n + 1), dtype=int)
    
    # Initialize gap penalties
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + scorer.get_score(seq1[i-1], '-')
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + scorer.get_score('-', seq2[j-1])
    
    # Fill DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + scorer.get_score(seq1[i-1], seq2[j-1])
            delete = dp[i-1][j] + scorer.get_score(seq1[i-1], '-')
            insert = dp[i][j-1] + scorer.get_score('-', seq2[j-1])
            dp[i][j] = max(match, delete, insert)
    
    return dp[m][n]

def compute_all_pairs(organisms: Dict[str, str], blosum_file: str) -> Dict[Tuple[str, str], int]:
    """Compute NW scores for all organism pairs."""
    blosum = load_blosum_matrix(blosum_file)
    scorer = BlosumScorer(blosum)
    species = list(organisms.keys())
    scores = {}
    
    for i in range(len(species)):
        for j in range(i, len(species)):
            score = needleman_wunsch(organisms[species[i]], organisms[species[j]], scorer)
            scores[(species[i], species[j])] = score
            if i != j:
                scores[(species[j], species[i])] = score
    return scores