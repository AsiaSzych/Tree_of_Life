"""Module for loading organism sequences and BLOSUM matrices from JSON files."""

import json
import logging
from pathlib import Path
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


class DataLoader:
    """Handles loading of organism sequences and BLOSUM substitution matrices."""
    
    def __init__(self, base_path: Path = Path(".")):
        """
        Initialize DataLoader with base path for file operations.
        
        Args:
            base_path: Base directory path for data files
        """
        self.base_path = base_path
    
    def load_organisms(self, filename: str = "organisms.json") -> Dict[str, str]:
        """
        Load organism sequences from JSON file.
        
        Args:
            filename: Name of the JSON file containing organism sequences
            
        Returns:
            Dictionary mapping species names to amino acid sequences
            
        Raises:
            FileNotFoundError: If the organisms file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        filepath = self.base_path / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                organisms = json.load(f)
            
            # Validate data structure
            if not isinstance(organisms, dict):
                raise ValueError(f"Expected dictionary in {filename}, got {type(organisms)}")
            
            for species, sequence in organisms.items():
                if not isinstance(species, str) or not isinstance(sequence, str):
                    raise ValueError(f"Invalid data types for species {species}")
                if not sequence:
                    raise ValueError(f"Empty sequence for species {species}")
            
            logger.info(f"Loaded {len(organisms)} organisms from {filename}")
            return organisms
            
        except FileNotFoundError:
            logger.error(f"Organisms file not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            raise
    
    def load_blosum_matrix(self, blosum_type: int = 62) -> Dict[str, int]:
        """
        Load BLOSUM substitution matrix from JSON file.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
            
        Returns:
            Dictionary with gap penalties and substitution scores
            
        Raises:
            ValueError: If blosum_type is not 50 or 62
            FileNotFoundError: If the BLOSUM file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if blosum_type not in [50, 62]:
            raise ValueError(f"Invalid BLOSUM type: {blosum_type}. Must be 50 or 62.")
        
        filename = f"blosum{blosum_type}.json"
        filepath = self.base_path / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                blosum = json.load(f)
            
            # Validate data structure
            if not isinstance(blosum, dict):
                raise ValueError(f"Expected dictionary in {filename}, got {type(blosum)}")
            
            # Convert all values to integers
            blosum_int = {}
            for key, value in blosum.items():
                if not isinstance(key, str) or len(key) not in [1, 2]:
                    raise ValueError(f"Invalid key format: {key}")
                try:
                    blosum_int[key] = int(value)
                except (TypeError, ValueError):
                    raise ValueError(f"Invalid score value for key {key}: {value}")
            
            logger.info(f"Loaded BLOSUM{blosum_type} matrix with {len(blosum_int)} entries")
            return blosum_int
            
        except FileNotFoundError:
            logger.error(f"BLOSUM file not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {filename}: {e}")
            raise