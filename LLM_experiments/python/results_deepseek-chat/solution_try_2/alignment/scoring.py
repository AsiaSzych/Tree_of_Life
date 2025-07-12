from typing import Dict

class BlosumScorer:
    def __init__(self, blosum_data: Dict[str, int]):
        """Initialize with BLOSUM matrix data."""
        self.substitution_scores = {}
        self.gap_penalties = {}
        
        for key, value in blosum_data.items():
            if len(key) == 1:
                self.gap_penalties[key] = value
            elif len(key) == 2:
                self.substitution_scores[key] = value
            else:
                raise ValueError(f"Invalid BLOSUM key length: {key}")
    
    def get_score(self, a: str, b: str) -> int:
        """Get substitution score for two amino acids."""
        if a == b:
            key = a + a
        else:
            key = a + b if a + b in self.substitution_scores else b + a
        return self.substitution_scores.get(key, 0)
    
    def get_gap_penalty(self, a: str) -> int:
        """Get gap penalty for an amino acid."""
        return self.gap_penalties.get(a, -1)  # Default gap penalty if not found