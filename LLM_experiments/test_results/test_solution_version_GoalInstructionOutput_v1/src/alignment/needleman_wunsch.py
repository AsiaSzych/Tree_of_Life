from typing import Dict

def calculate_alignment_score(seq1: str, seq2: str, scoring_matrix: Dict[str, int]) -> int:
    """
    Calculates the optimal global alignment score using the Needleman-Wunsch algorithm.

    Args:
        seq1: The first sequence (protein).
        seq2: The second sequence (protein).
        scoring_matrix: A dictionary containing substitution scores (e.g., "AA")
                        and character-dependent gap penalties (e.g., "A").

    Returns:
        The final integer alignment score.
    """
    n, m = len(seq1), len(seq2)
    dp_matrix = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        dp_matrix[i][0] = dp_matrix[i - 1][0] + scoring_matrix[seq1[i - 1]]
    for j in range(1, m + 1):
        dp_matrix[0][j] = dp_matrix[0][j - 1] + scoring_matrix[seq2[j - 1]]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1, char2 = seq1[i - 1], seq2[j - 1]
            match_key, rev_match_key = char1 + char2, char2 + char1
            match_score = scoring_matrix.get(match_key, scoring_matrix.get(rev_match_key))
            
            if match_score is None:
                raise KeyError(f"Scoring for pair '{match_key}' or '{rev_match_key}' not found in matrix.")

            score_diag = dp_matrix[i - 1][j - 1] + match_score
            score_up = dp_matrix[i - 1][j] + scoring_matrix[char1]
            score_left = dp_matrix[i][j - 1] + scoring_matrix[char2]

            dp_matrix[i][j] = max(score_diag, score_up, score_left)

    return dp_matrix[n][m]