"""Example script to create a sample thresholds file."""

import json
from pathlib import Path


def create_example_thresholds(scores_file: str = "organisms_scores_blosum62.json"):
    """
    Create example thresholds file based on score range.
    
    Args:
        scores_file: Path to scores JSON file
    """
    # Load scores to get range
    with open(scores_file, 'r') as f:
        scores_dict = json.load(f)
    
    scores = list(scores_dict.values())
    min_score = min(scores)
    max_score = max(scores)
    score_range = max_score - min_score
    
    print(f"Score range: {min_score} - {max_score}")
    
    # Create thresholds at different percentiles
    thresholds = [
        int(min_score + score_range * 0.2),  # 20th percentile
        int(min_score + score_range * 0.4),  # 40th percentile
        int(min_score + score_range * 0.6),  # 60th percentile
        int(min_score + score_range * 0.8),  # 80th percentile
        int(min_score + score_range * 0.9),  # 90th percentile
    ]
    
    # Save to file
    with open("thresholds.txt", 'w') as f:
        for threshold in thresholds:
            f.write(f"{threshold}\n")
    
    print(f"Created thresholds.txt with values: {thresholds}")


if __name__ == "__main__":
    create_example_thresholds()