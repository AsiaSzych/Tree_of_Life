# src/utils.py

import json
import os # Added for directory creation
from typing import Any

def load_json_data(filepath: str) -> dict[str, Any]:
    """
    Loads data from a JSON file.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        dict[str, Any]: The loaded JSON data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        Exception: For other unexpected I/O errors.
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


def save_json_data(filepath: str, data: dict[str, Any]) -> None:
    """
    Saves data to a JSON file. Creates parent directories if they don't exist.

    Args:
        filepath (str): The path to the JSON file where data will be saved.
        data (dict[str, Any]): The dictionary data to save.

    Raises:
        IOError: If there's an error writing to the file.
        Exception: For other unexpected errors during directory creation or saving.
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4) # Use indent for pretty printing
    except IOError as e:
        raise IOError(f"Error: Could not write data to '{filepath}': {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while saving to '{filepath}': {e}")
