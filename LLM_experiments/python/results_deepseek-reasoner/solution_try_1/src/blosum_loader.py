import json
from typing import Dict, Tuple

class BlosumLoader:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as f:
            self.blosum_data = json.load(f)
    
    def get_gap_penalty(self, amino_acid: str) -> int:
        return self.blosum_data.get(amino_acid, 0)
    
    def get_substitution_score(self, aa1: str, aa2: str) -> int:
        return self.blosum_data.get(
            aa1 + aa2,
            self.blosum_data.get(aa2 + aa1, 0)
        )