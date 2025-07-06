# src/alignment.py

from typing import Dict

class ScoringHandler:
    """A handler to easily retrieve scores from a flattened BLOSUM dictionary."""
    def __init__(self, blosum_data: Dict[str, int]):
        self._data = blosum_data

    def get_substitution_score(self, char1: str, char2: str) -> int:
        key1 = char1 + char2
        key2 = char2 + char1
        return self._data.get(key1, self._data.get(key2, 0))

    def get_gap_score(self, char: str) -> int:
        return self._data.get(char, 0)


def calculate_nw_score(
    seq1: str,
    seq2: str,
    scoring_handler: ScoringHandler
) -> int:
    """Calculates the Needleman-Wunsch alignment score for two sequences."""
    n = len(seq1)
    m = len(seq2)
    dp_matrix = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp_matrix[i][0] = dp_matrix[i - 1][0] + scoring_handler.get_gap_score(seq1[i - 1])

    for j in range(1, m + 1):
        dp_matrix[0][j] = dp_matrix[0][j - 1] + scoring_handler.get_gap_score(seq2[j - 1])

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1, char2 = seq1[i - 1], seq2[j - 1]
            match_mismatch = dp_matrix[i - 1][j - 1] + scoring_handler.get_substitution_score(char1, char2)
            deletion = dp_matrix[i - 1][j] + scoring_handler.get_gap_score(char1)
            insertion = dp_matrix[i][j - 1] + scoring_handler.get_gap_score(char2)
            dp_matrix[i][j] = max(match_mismatch, deletion, insertion)

    return dp_matrix[n][m]