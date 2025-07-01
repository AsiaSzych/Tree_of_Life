import json
from pathlib import Path
from typing import Dict, List, Tuple

def load_sequences(file_path: Path) -> Dict[str, str]:
    """Loads species sequences from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return {}

def load_scoring_matrix(file_path: Path) -> Dict[str, int]:
    """Loads the BLOSUM scoring matrix from a JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return {}

def save_scores_to_json(scores: Dict[str, Dict[str, int]], species_list: List[str], output_path: Path):
    """Saves alignment scores to a JSON file in a flat key-value format."""
    import itertools
    flat_scores = {f"{s1}_{s2}": scores[s1][s2] for s1, s2 in itertools.combinations(species_list, 2)}
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(flat_scores, f, indent=4)
        print(f"\nSuccessfully saved scores to: {output_path}")
    except IOError as e:
        print(f"Error: Could not write to file {output_path}. Reason: {e}")

def load_scores_from_json(file_path: Path) -> Tuple[Dict[str, Dict[str, int]], List[str]]:
    """Loads pairwise scores from a flat JSON file and reconstructs a nested dict."""
    try:
        with open(file_path, 'r') as f:
            flat_scores = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return {}, []
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} is not a valid JSON file.")
        return {}, []

    scores_dict, species_set = {}, set()
    for key, score in flat_scores.items():
        species1, species2 = key.split('_')
        species_set.update([species1, species2])
        scores_dict.setdefault(species1, {})[species2] = score
        scores_dict.setdefault(species2, {})[species1] = score
    return scores_dict, sorted(list(species_set))

def save_text_file(content: str, output_path: Path):
    """Saves a string content to a text file."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(content)
        print(f"Successfully saved file to: {output_path}")
    except IOError as e:
        print(f"Error: Could not write to file {output_path}. Reason: {e}")

def load_thresholds(file_path: Path) -> List[int]:
    """Loads integer thresholds from a text file, one per line."""
    if not file_path.exists():
        print(f"Error: Threshold file not found at {file_path}")
        return []
    thresholds = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip():
                    thresholds.append(int(line.strip()))
        return thresholds
    except (IOError, ValueError) as e:
        print(f"Error reading or parsing threshold file {file_path}: {e}")
        return []

def save_clusters_to_json(clusters_data: Dict[int, List[List[str]]], output_path: Path):
    """Saves the calculated clusters to a JSON file."""
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(clusters_data, f, indent=4)
        print(f"\nSuccessfully saved cluster data to: {output_path}")
    except IOError as e:
        print(f"Error: Could not write to file {output_path}. Reason: {e}")