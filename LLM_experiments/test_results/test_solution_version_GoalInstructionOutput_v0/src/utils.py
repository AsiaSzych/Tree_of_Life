# src/utils.py

import json
from typing import Dict, Any, List

def load_json_data(file_path: str) -> Dict[str, Any]:
    """
    Loads data from a JSON file with error handling.
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} is not a valid JSON file.")
        raise

def load_thresholds(file_path: str) -> List[float]:
    """
    Loads clustering thresholds from a text file.
    """
    thresholds = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    thresholds.append(float(line))
        return thresholds
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        raise
    except ValueError as e:
        print(f"Error: Could not parse a value in {file_path}. Details: {e}")
        raise