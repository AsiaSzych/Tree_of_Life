"""Handles loading and accessing BLOSUM substitution matrices."""

import json
from pathlib import Path
from typing import Dict

def load_blosum_matrix(file_path: str) -> Dict[str, int]:
    """Load BLOSUM matrix from JSON file.
    
    Args:
        file_path: Path to BLOSUM JSON file
        
    Returns:
        Dictionary with substitution scores
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"BLOSUM file not found: {file_path}")
    
    with open(path, 'r') as f:
        matrix = json.load(f)
    
    # Validate matrix contains at least some expected keys
    if not any(len(k) in (1, 2) for k in matrix):
        raise ValueError("Invalid BLOSUM matrix format")
    
    return matrix

def get_substitution_score(matrix: Dict[str, int], a: str, b: str) -> int:
    """Get substitution score for two amino acids.
    
    Args:
        matrix: BLOSUM matrix
        a: First amino acid
        b: Second amino acid
        
    Returns:
        Substitution score
    """
    if a == b:
        key = a + a  # e.g. 'aa'
    else:
        key = a + b if a + b in matrix else b + a
    
    return matrix.get(key, -4)  # Default penalty if pair not found

def get_deletion_score(matrix: Dict[str, int], a: str) -> int:
    """Get deletion score for an amino acid.
    
    Args:
        matrix: BLOSUM matrix
        a: Amino acid
        
    Returns:
        Deletion score
    """
    return matrix.get(a, -4)  # Default penalty if not found