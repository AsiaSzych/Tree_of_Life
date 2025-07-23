"""
Module for loading input data from JSON files.
"""
import json
from pathlib import Path
from typing import Dict


class DataLoader:
    """Handles loading of organism sequences and BLOSUM matrices."""
    
    @staticmethod
    def load_organisms(filepath: str = "organisms.json") -> Dict[str, str]:
        """
        Load organism sequences from JSON file.
        
        Args:
            filepath: Path to the organisms JSON file
            
        Returns:
            Dictionary mapping species names to amino acid sequences
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Organisms file not found: {filepath}")
        
        with open(path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def load_blosum_matrix(blosum_type: int = 62) -> Dict[str, int]:
        """
        Load BLOSUM substitution matrix from JSON file.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
            
        Returns:
            Dictionary with gap penalties and substitution scores
        """
        filepath = f"blosum{blosum_type}.json"
        path = Path(filepath)
        
        if not path.exists():
            raise FileNotFoundError(f"BLOSUM matrix file not found: {filepath}")
        
        with open(path, 'r') as f:
            return json.load(f)