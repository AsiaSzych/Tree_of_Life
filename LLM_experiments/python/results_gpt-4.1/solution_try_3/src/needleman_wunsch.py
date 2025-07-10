import json
from typing import Dict

def load_organisms(filepath: str) -> Dict[str, str]:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def load_blosum(filepath: str) -> Dict[str, int]:
    with open(filepath, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {k: int(v) for k, v in raw.items()}

def needleman_wunsch(seq1: str, seq2: str, blosum: Dict[str, int]) -> int:
    m, n = len(seq1), len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] + blosum[seq1[i - 1]]
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] + blosum[seq2[j - 1]]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            char1 = seq1[i - 1]
            char2 = seq2[j - 1]
            match_key = char1 + char2
            match_score = blosum[match_key]
            delete_score = blosum[char1]
            insert_score = blosum[char2]
            dp[i][j] = max(
                dp[i - 1][j - 1] + match_score,
                dp[i - 1][j] + delete_score,
                dp[i][j - 1] + insert_score
            )
    return dp[m][n]

def compute_all_pairwise_scores(
    organisms: Dict[str, str], blosum: Dict[str, int]
) -> Dict[str, Dict[str, int]]:
    species = list(organisms.keys())
    scores = {sp1: {} for sp1 in species}
    for i, sp1 in enumerate(species):
        seq1 = organisms[sp1]
        for j, sp2 in enumerate(species):
            if sp2 in scores[sp1]:
                continue
            seq2 = organisms[sp2]
            score = needleman_wunsch(seq1, seq2, blosum)
            scores[sp1][sp2] = score
            scores[sp2][sp1] = score
    return scores

def flatten_scores(scores: Dict[str, Dict[str, int]]) -> Dict[str, int]:
    """
    Flatten nested scores dict to {"species1_species2": score, ...}
    Only unique pairs (alphabetically sorted) are included.
    """
    flat = {}
    for sp1 in scores:
        for sp2 in scores[sp1]:
            if sp1 <= sp2:  # Avoid duplicates
                key = f"{sp1}_{sp2}"
            else:
                key = f"{sp2}_{sp1}"
            flat[key] = scores[sp1][sp2]
    # Remove duplicates by keeping only one direction
    return dict(sorted(flat.items()))

def save_scores_to_json(flat_scores: Dict[str, int], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(flat_scores, f, indent=2)