import json
from pathlib import Path
from typing import Dict, Any, Tuple

def read_organisms(file_path: str) -> Dict[str, str]:
    """Read organisms JSON file and return species:sequence mapping."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Organisms file not found: {file_path}")
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    if not isinstance(data, dict):
        raise ValueError("Invalid organisms.json format")
    
    return data

def read_blosum_matrix(file_path: str) -> Dict[str, int]:
    """Read BLOSUM matrix JSON file and return scoring dictionary."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"BLOSUM file not found: {file_path}")
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    if not isinstance(data, dict):
        raise ValueError("Invalid BLOSUM matrix format")
    
    return data

def save_scores_to_json(scores: Dict[Tuple[str, str], int], blosum_type: str, output_dir: str = "./output") -> None:
    """
    Save alignment scores to JSON file with format {species1_species2: score}.
    
    Args:
        scores: Dictionary of {(species1, species2): score} pairs
        blosum_type: Type of BLOSUM matrix used (50 or 62)
        output_dir: Directory to save output files (default: ./output)
    """
    Path(output_dir).mkdir(exist_ok=True)
    
    # Convert tuple keys to string keys with underscore
    formatted_scores = {
        f"{species1}_{species2}": score 
        for (species1, species2), score in scores.items()
    }
    
    output_path = Path(output_dir) / f"organisms_scores_blosum{blosum_type}.json"
    
    with open(output_path, 'w') as f:
        json.dump(formatted_scores, f, indent=4)