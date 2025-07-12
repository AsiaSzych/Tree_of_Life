from typing import Dict, Tuple
from .scoring import BlosumScorer

def needleman_wunsch(seq1: str, seq2: str, scorer: BlosumScorer) -> int:
    """Calculate Needleman-Wunsch alignment score for two sequences."""
    m, n = len(seq1), len(seq2)
    
    # Initialize DP matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Fill first row and column with gap penalties
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + scorer.get_gap_penalty(seq1[i-1])
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + scorer.get_gap_penalty(seq2[j-1])
    
    # Fill DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + scorer.get_score(seq1[i-1], seq2[j-1])
            delete = dp[i-1][j] + scorer.get_gap_penalty(seq1[i-1])
            insert = dp[i][j-1] + scorer.get_gap_penalty(seq2[j-1])
            dp[i][j] = max(match, delete, insert)
    
    return dp[m][n]

def calculate_all_pairs(organisms: Dict[str, str], scorer: BlosumScorer) -> Dict[Tuple[str, str], int]:
    """Calculate NW scores for all pairs of organisms."""
    species = list(organisms.keys())
    scores = {}
    
    for i in range(len(species)):
        for j in range(i, len(species)):
            seq1 = organisms[species[i]]
            seq2 = organisms[species[j]]
            score = needleman_wunsch(seq1, seq2, scorer)
            scores[(species[i], species[j])] = score
            if i != j:  # Avoid duplicate calculations
                scores[(species[j], species[i])] = score
    
    return scores