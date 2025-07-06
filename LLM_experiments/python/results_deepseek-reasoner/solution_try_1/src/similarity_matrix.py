from typing import Dict, List

class SimilarityMatrix:
    def __init__(self, species: List[str]):
        self.species_index = {s: idx for idx, s in enumerate(species)}
        self.matrix = [[0] * len(species) for _ in range(len(species))]
    
    def add_score(self, species1: str, species2: str, score: int):
        i = self.species_index[species1]
        j = self.species_index[species2]
        self.matrix[i][j] = score
        self.matrix[j][i] = score
    
    def get_score(self, species1: str, species2: str) -> int:
        i = self.species_index[species1]
        j = self.species_index[species2]
        return self.matrix[i][j]