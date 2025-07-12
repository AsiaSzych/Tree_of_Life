from typing import Dict

class BlosumScorer:
    def __init__(self, blosum_matrix: Dict[str, int]):
        self.matrix = blosum_matrix
        
    def get_score(self, a: str, b: str) -> int:
        """Get substitution score for two amino acids."""
        if a == '-' and b == '-':
            return 0
        if a == '-':
            return self.matrix.get(b, -4)  # Default gap penalty
        if b == '-':
            return self.matrix.get(a, -4)
        if a == b:
            return self.matrix.get(a + b, self.matrix.get(a, -4))
        return self.matrix.get(a + b, self.matrix.get(b + a, -4))