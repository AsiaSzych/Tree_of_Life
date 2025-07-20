import json
from typing import Dict, Tuple

def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_organisms(filepath: str) -> Dict[str, str]:
    return load_json(filepath)

def load_blosum(filepath: str) -> Dict[str, int]:
    blosum_raw = load_json(filepath)
    return {k: int(v) for k, v in blosum_raw.items()}

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
            match = score[i - 1][j - 1] + blosum[seq1[i - 1] + seq2[j - 1]]
            delete = score[i - 1][j] + blosum[seq1[i - 1]]
            insert = score[i][j - 1] + blosum[seq2[j - 1]]
            score[i][j] = max(match, delete, insert)
    return int(score[m][n])

def compute_all_pairwise_scores(
    organisms: Dict[str, str], blosum: Dict[str, int]
) -> Dict[str, int]:
    species = list(organisms.keys())
    scores = {}
    for i, sp1 in enumerate(species):
        seq1 = organisms[sp1]
        for j, sp2 in enumerate(species):
            if j < i:
                key = f"{sp2}_{sp1}"
                scores[f"{sp1}_{sp2}"] = scores[key]
            else:
                seq2 = organisms[sp2]
                score = needleman_wunsch(seq1, seq2, blosum)
                scores[f"{sp1}_{sp2}"] = score
    return scores

def save_scores_to_json(scores: Dict[str, int], output_path: str) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)