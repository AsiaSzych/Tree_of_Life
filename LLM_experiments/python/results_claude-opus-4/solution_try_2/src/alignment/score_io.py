"""
Module for handling input/output operations for alignment scores.
"""
import json
from pathlib import Path
from typing import Dict, Tuple


def save_scores_to_json(
    pairwise_scores: Dict[Tuple[str, str], int],
    blosum_file: str,
    output_dir: str = "."
) -> str:
    """
    Save pairwise alignment scores to a JSON file.
    
    Args:
        pairwise_scores: Dictionary mapping species pairs to alignment scores
        blosum_file: Name of the BLOSUM file used (e.g., 'blosum62.json')
        output_dir: Directory to save the output file
        
    Returns:
        Path to the saved file
    """
    # Extract BLOSUM version from filename
    blosum_version = Path(blosum_file).stem  # e.g., 'blosum62' from 'blosum62.json'
    
    # Create output filename
    output_filename = f"organisms_scores_{blosum_version}.json"
    output_path = Path(output_dir) / output_filename
    
    # Convert tuple keys to concatenated string keys
    formatted_scores = {}
    for (species1, species2), score in pairwise_scores.items():
        # Skip self-alignments if needed, or include them
        key = f"{species1}_{species2}"
        formatted_scores[key] = score
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save to JSON file
    with open(output_path, 'w') as f:
        json.dump(formatted_scores, f, indent=2)
    
    return str(output_path)


def load_scores_from_json(filename: str) -> Dict[str, int]:
    """
    Load pairwise alignment scores from a JSON file.
    
    Args:
        filename: Path to the JSON file containing scores
        
    Returns:
        Dictionary mapping concatenated species names to scores
    """
    file_path = Path(filename)
    if not file_path.exists():
        raise FileNotFoundError(f"Scores file not found: {filename}")
    
    with open(file_path, 'r') as f:
        return json.load(f)