# filename: alignment.py
import numpy as np

def get_score(char1: str, char2: str, scores: dict) -> int:
    return scores.get(char1 + char2, scores[char2 + char1])

def needleman_wunsch(seq1: str, seq2: str, scores: dict) -> int:
    len_seq1, len_seq2 = len(seq1), len(seq2)
    dp_matrix = np.zeros((len_seq1 + 1, len_seq2 + 1), dtype=int)
    for j in range(1, len_seq2 + 1):
        dp_matrix[0, j] = dp_matrix[0, j - 1] + scores[seq2[j - 1]]
    for i in range(1, len_seq1 + 1):
        dp_matrix[i, 0] = dp_matrix[i - 1, 0] + scores[seq1[i - 1]]
    for i in range(1, len_seq1 + 1):
        for j in range(1, len_seq2 + 1):
            char1, char2 = seq1[i - 1], seq2[j - 1]
            match_score = dp_matrix[i - 1, j - 1] + get_score(char1, char2, scores)
            delete_score = dp_matrix[i - 1, j] + scores[char1]
            insert_score = dp_matrix[i, j - 1] + scores[char2]
            dp_matrix[i, j] = max(match_score, delete_score, insert_score)
    return dp_matrix[len_seq1, len_seq2]