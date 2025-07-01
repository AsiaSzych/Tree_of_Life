# src/alignment.py

from typing import Dict

def calculate_nw_score(seq1: str, seq2: str, scores: Dict[str, int]) -> int:
    """
    Calculates the similarity score of two sequences using the
    Needleman-Wunsch algorithm.
    """
    n = len(seq1)
    m = len(seq2)
    dp_matrix = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp_matrix[i][0] = dp_matrix[i-1][0] + scores[seq1[i-1]]
    for j in range(1, m + 1):
        dp_matrix[0][j] = dp_matrix[0][j-1] + scores[seq2[j-1]]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1, char2 = seq1[i-1], seq2[j-1]
            match_key, rev_match_key = char1 + char2, char2 + char1
            match_score = scores.get(match_key, scores.get(rev_match_key))
            
            diagonal_score = dp_matrix[i-1][j-1] + match_score
            delete_score = dp_matrix[i-1][j] + scores[char1]
            insert_score = dp_matrix[i][j-1] + scores[char2]
            
            dp_matrix[i][j] = max(diagonal_score, delete_score, insert_score)

    return dp_matrix[n][m]