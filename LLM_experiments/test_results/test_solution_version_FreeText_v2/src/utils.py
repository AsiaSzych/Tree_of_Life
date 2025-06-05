# src/utils.py
import json
import os
from typing import Any, Dict

def load_json_data(filepath: str) -> Dict[str, Any]:
    """
    Loads JSON data from a specified file path.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The loaded JSON data.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        Exception: For other unexpected errors during file reading.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: File not found at '{filepath}'")
    except json.JSONDecodeError:
        raise json.JSONDecodeError(f"Error: Invalid JSON format in '{filepath}'", doc="", pos=0)
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading '{filepath}': {e}")

def save_json_data(data: Dict[str, Any], filepath: str) -> None:
    """
    Saves a dictionary as JSON data to a specified file path.

    Args:
        data (Dict[str, Any]): The dictionary to save.
        filepath (str): The path to the output JSON file.
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Scores successfully saved to '{filepath}'")
    except IOError as e:
        raise IOError(f"Error writing to file '{filepath}': {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while saving to '{filepath}': {e}")