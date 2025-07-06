import json
from typing import Dict


def load_sequences(filepath: str) -> Dict[str, str]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_blosum(filepath: str) -> Dict[str, int]:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {k: int(v) for k, v in data.items()}


def needleman_wunsch(
    seq1: str, seq2: str, blosum: Dict[str, int]
) -> int:
    m, n = len(seq1), len(seq2)
    score = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        score[i][0] = score[i - 1][0] + blosum[seq1[i - 1]]

    for j in range(1, n + 1):
        score[0][j] = score[0][j - 1] + blosum[seq2[j - 1]]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            char1 = seq1[i - 1]
            char2 = seq2[j - 1]
            match_key = char1 + char2
            match = score[i - 1][j - 1] + blosum[match_key]
            delete = score[i - 1][j] + blosum[char1]
            insert = score[i][j - 1] + blosum[char2]
            score[i][j] = max(match, delete, insert)

    return int(score[m][n])