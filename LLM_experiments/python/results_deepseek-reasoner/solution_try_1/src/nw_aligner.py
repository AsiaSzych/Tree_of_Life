from typing import Dict
from blosum_loader import BlosumLoader

def needleman_wunsch(seq1: str, seq2: str, blosum: BlosumLoader) -> int:
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i-1][0] + blosum.get_gap_penalty(seq1[i-1])
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j-1] + blosum.get_gap_penalty(seq2[j-1])
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = dp[i-1][j-1] + blosum.get_substitution_score(seq1[i-1], seq2[j-1])
            gap1 = dp[i-1][j] + blosum.get_gap_penalty(seq1[i-1])
            gap2 = dp[i][j-1] + blosum.get_gap_penalty(seq2[j-1])
            dp[i][j] = max(match, gap1, gap2)
    
    return dp[m][n]