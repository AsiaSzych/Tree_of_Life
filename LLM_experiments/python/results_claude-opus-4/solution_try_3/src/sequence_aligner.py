"""Main module for calculating pairwise sequence alignments."""

import json
import logging
from itertools import combinations
from pathlib import Path
from typing import Dict, Tuple, Optional

from .data_loader import DataLoader
from .needleman_wunsch import NeedlemanWunsch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SequenceAligner:
    """Manages pairwise sequence alignment for multiple species."""
    
    def __init__(self, blosum_type: int = 62, base_path: Path = Path(".")):
        """
        Initialize SequenceAligner.
        
        Args:
            blosum_type: BLOSUM matrix type (50 or 62)
            base_path: Base directory path for data files
        """
        self.blosum_type = blosum_type
        self.base_path = base_path
        self.data_loader = DataLoader(base_path)
        self.organisms: Optional[Dict[str, str]] = None
        self.aligner: Optional[NeedlemanWunsch] = None
        self.alignment_scores: Dict[Tuple[str, str], int] = {}
    
    def load_data(self) -> None:
        """Load organisms and BLOSUM matrix data."""
        logger.info("Loading organism sequences...")
        self.organisms = self.data_loader.load_organisms()
        
        logger.info(f"Loading BLOSUM{self.blosum_type} matrix...")
        blosum_matrix = self.data_loader.load_blosum_matrix(self.blosum_type)
        self.aligner = NeedlemanWunsch(blosum_matrix)
    
    def calculate_all_alignments(self) -> Dict[Tuple[str, str], int]:
        """
        Calculate alignment scores for all pairs of species.
        
        Returns:
            Dictionary mapping species pairs to alignment scores
        """
        if not self.organisms or not self.aligner:
            raise RuntimeError("Data not loaded. Call load_data() first.")
        
        species_list = list(self.organisms.keys())
        total_pairs = len(list(combinations(species_list, 2)))
        logger.info(f"Calculating alignments for {total_pairs} species pairs...")
        
        # Calculate alignment for each pair
        for i, (species1, species2) in enumerate(combinations(species_list, 2)):
            seq1 = self.organisms[species1]
            seq2 = self.organisms[species2]
            
            score = self.aligner.align(seq1, seq2)
            
            # Store score with ordered tuple key for consistency
            key = (species1, species2) if species1 < species2 else (species2, species1)
            self.alignment_scores[key] = score
            
            if (i + 1) % 10 == 0:
                logger.info(f"Processed {i + 1}/{total_pairs} pairs...")
        
        logger.info(f"Completed all {total_pairs} alignments")
        return self.alignment_scores
    
    def save_scores(self, filename: Optional[str] = None) -> str:
        """
        Save alignment scores to JSON file.
        
        Args:
            filename: Optional custom filename. If not provided, uses default naming.
            
        Returns:
            Path to the saved file
            
        Raises:
            RuntimeError: If no scores have been calculated
        """
        if not self.alignment_scores:
            raise RuntimeError("No alignment scores to save. Run calculate_all_alignments() first.")
        
        # Use default filename if not provided
        if filename is None:
            filename = f"organisms_scores_blosum{self.blosum_type}.json"
        
        filepath = self.base_path / filename
        
        # Convert tuple keys to string keys for JSON serialization
        json_scores = {}
        for (species1, species2), score in self.alignment_scores.items():
            # Create key with consistent ordering (alphabetical)
            key = f"{species1}_{species2}"
            json_scores[key] = score
        
        # Save to file
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_scores, f, indent=2, sort_keys=True)
            
            logger.info(f"Saved {len(json_scores)} alignment scores to {filepath}")
            return str(filepath)
            
        except IOError as e:
            logger.error(f"Failed to save scores to {filepath}: {e}")
            raise
    
    def load_scores(self, filename: Optional[str] = None) -> Dict[Tuple[str, str], int]:
        """
        Load previously saved alignment scores from JSON file.
        
        Args:
            filename: Optional custom filename. If not provided, uses default naming.
            
        Returns:
            Dictionary mapping species pairs to alignment scores
        """
        if filename is None:
            filename = f"organisms_scores_blosum{self.blosum_type}.json"
        
        filepath = self.base_path / filename
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_scores = json.load(f)
            
            # Convert string keys back to tuple keys
            self.alignment_scores = {}
            for key_str, score in json_scores.items():
                species1, species2 = key_str.split('_', 1)
                # Maintain consistent ordering
                key = (species1, species2) if species1 < species2 else (species2, species1)
                self.alignment_scores[key] = score
            
            logger.info(f"Loaded {len(self.alignment_scores)} alignment scores from {filepath}")
            return self.alignment_scores
            
        except FileNotFoundError:
            logger.error(f"Score file not found: {filepath}")
            raise
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"Invalid score file format: {e}")
            raise
    
    def get_score(self, species1: str, species2: str) -> int:
        """
        Get alignment score for a specific species pair.
        
        Args:
            species1: First species name
            species2: Second species name
            
        Returns:
            Alignment score
            
        Raises:
            KeyError: If the species pair hasn't been aligned
        """
        # Handle same species comparison
        if species1 == species2:
            if species1 not in self.organisms:
                raise KeyError(f"Species {species1} not found")
            return self.aligner.align(self.organisms[species1], self.organisms[species1])
        
        # Order the tuple key consistently
        key = (species1, species2) if species1 < species2 else (species2, species1)
        
        if key not in self.alignment_scores:
            raise KeyError(f"No alignment score found for pair: {species1}, {species2}")
        
        return self.alignment_scores[key]


def main():
    """Example usage demonstrating both BLOSUM50 and BLOSUM62 calculations."""
    import json
    
    # Create test data
    test_organisms = {
        "testspecies1": "aabaab",
        "testspecies2": "ababaa",
        "testspecies3": "aabbaa"
    }
    
    test_blosum = {
        "a": -1,
        "b": -2,
        "ab": -3,
        "ba": -3,
        "aa": 2,
        "bb": 3
    }
    
    # Save test data
    with open("organisms.json", "w") as f:
        json.dump(test_organisms, f)
    
    # Save as both BLOSUM50 and BLOSUM62 for testing
    with open("blosum50.json", "w") as f:
        json.dump(test_blosum, f)
    
    with open("blosum62.json", "w") as f:
        json.dump(test_blosum, f)
    
    # Run alignment with BLOSUM62
    logger.info("=== Running with BLOSUM62 ===")
    aligner62 = SequenceAligner(blosum_type=62)
    aligner62.load_data()
    scores62 = aligner62.calculate_all_alignments()
    saved_file62 = aligner62.save_scores()
    
    # Print results
    print("\nBLOSUM62 Results:")
    for (species1, species2), score in scores62.items():
        print(f"{species1} vs {species2}: {score}")
    print(f"Saved to: {saved_file62}")
    
    # Run alignment with BLOSUM50
    logger.info("\n=== Running with BLOSUM50 ===")
    aligner50 = SequenceAligner(blosum_type=50)
    aligner50.load_data()
    scores50 = aligner50.calculate_all_alignments()
    saved_file50 = aligner50.save_scores()
    
    # Print results
    print("\nBLOSUM50 Results:")
    for (species1, species2), score in scores50.items():
        print(f"{species1} vs {species2}: {score}")
    print(f"Saved to: {saved_file50}")
    
    # Demonstrate loading saved scores
    logger.info("\n=== Testing score loading ===")
    new_aligner = SequenceAligner(blosum_type=62)
    loaded_scores = new_aligner.load_scores()
    print(f"\nLoaded {len(loaded_scores)} scores from file")


if __name__ == "__main__":
    main()