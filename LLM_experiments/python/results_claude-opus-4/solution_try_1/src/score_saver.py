"""
Module for saving similarity scores to JSON files.
"""
import json
from pathlib import Path
from typing import Dict, Tuple
import logging


class ScoreSaver:
    """Handles saving of similarity scores to JSON files."""
    
    def __init__(self):
        """Initialize the score saver."""
        self.logger = logging.getLogger(__name__)
    
    def save_scores(self, scores: Dict[Tuple[str, str], int], blosum_type: int) -> str:
        """
        Save similarity scores to a JSON file.
        
        Args:
            scores: Dictionary mapping species pairs (tuple) to alignment scores
            blosum_type: BLOSUM matrix type (50 or 62)
            
        Returns:
            Path to the saved file
        """
        # Prepare output data with concatenated keys
        output_data = {}
        
        for (species1, species2), score in scores.items():
            # Create key by concatenating species names with underscore
            key = f"{species1}_{species2}"
            output_data[key] = score
        
        # Create output filename
        output_filename = f"organisms_scores_blosum{blosum_type}.json"
        output_path = Path(output_filename)
        
        # Save to file
        try:
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            self.logger.info(f"Saved {len(output_data)} scores to {output_filename}")
            return str(output_path)
            
        except Exception as e:
            self.logger.error(f"Error saving scores to file: {e}")
            raise
    
    @staticmethod
    def load_scores(blosum_type: int) -> Dict[str, int]:
        """
        Load previously saved scores from JSON file.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
            
        Returns:
            Dictionary with concatenated species names as keys and scores as values
        """
        filename = f"organisms_scores_blosum{blosum_type}.json"
        path = Path(filename)
        
        if not path.exists():
            raise FileNotFoundError(f"Scores file not found: {filename}")
        
        with open(path, 'r') as f:
            return json.load(f)