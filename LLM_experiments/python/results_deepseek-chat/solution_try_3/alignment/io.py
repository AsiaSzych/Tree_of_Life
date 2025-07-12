"""Handles input/output operations for sequence data."""

import json
from pathlib import Path
from typing import Dict, Tuple

def load_organisms(file_path: str) -> Dict[str, str]:
    """Load organisms data from JSON file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Organisms file not found: {file_path}")
    with open(path, 'r') as f:
        return json.load(f)

def save_scores_to_json(scores: Dict[Tuple[str, str], int], output_path: str) -> None:
    """Save alignment scores to JSON file."""
    formatted_scores = {f"{s1}_{s2}": score for (s1, s2), score in scores.items()}
    with open(output_path, 'w') as f:
        json.dump(formatted_scores, f, indent=4)