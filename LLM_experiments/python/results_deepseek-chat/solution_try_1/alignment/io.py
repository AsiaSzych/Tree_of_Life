import json
from pathlib import Path
from typing import Dict, List, Tuple

def load_organisms(file_path: str) -> Dict[str, str]:
    """Load organism data from JSON file."""
    path = Path(file_path)
    with path.open('r') as f:
        return json.load(f)

def load_blosum_matrix(file_path: str) -> Dict[str, int]:
    """Load BLOSUM substitution matrix from JSON file."""
    path = Path(file_path)
    with path.open('r') as f:
        return json.load(f)

def save_scores(scores: Dict[Tuple[str, str], int], blosum_type: str) -> None:
    """Save alignment scores to JSON file."""
    formatted = {f"{k[0]}_{k[1]}": int(v) for k, v in scores.items()}
    output_path = Path(f"./outputs/organisms_scores_blosum{blosum_type}.json")
    with output_path.open('w') as f:
        json.dump(formatted, f, indent=2)

def load_thresholds(file_path: str) -> List[int]:
    """Load thresholds from text file (one per line)."""
    path = Path(file_path)
    with path.open('r') as f:
        return [int(line.strip()) for line in f if line.strip()]