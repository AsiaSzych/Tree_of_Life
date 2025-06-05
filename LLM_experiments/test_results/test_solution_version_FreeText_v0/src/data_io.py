# src/data_io.py

import json
import os
from typing import Dict, Tuple, List

def load_organisms(filepath: str) -> Dict[str, str]:
    """
    Loads species names and their DNA sequences from a JSON file.

    Args:
        filepath (str): The path to the organisms JSON file.

    Returns:
        Dict[str, str]: A dictionary where keys are species names and values are DNA sequences.

    Raises:
        FileNotFoundError: If the organisms file does not exist.
        json.JSONDecodeError: If the organisms file is not valid JSON.
        ValueError: If the organisms file has an invalid structure or content.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Organisms file not found at: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            organisms_data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in organisms file {filepath}: {e}", e.doc, e.pos)

    if not isinstance(organisms_data, dict):
        raise ValueError(f"Organisms file {filepath} must contain a JSON object (dictionary).")

    for key, value in organisms_data.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError(
                f"Organisms file {filepath} contains invalid key-value pair: '{key}': {value}. "
                "Keys (species names) and values (DNA sequences) must be strings."
            )
    return organisms_data

def save_pairwise_scores(
    scores: Dict[Tuple[str, str], int],
    output_filepath: str
) -> None:
    """
    Saves the calculated pairwise Needleman-Wunsch scores to a JSON file.

    The output JSON file will have keys as concatenated species names (e.g., "species1_species2")
    and values as the alignment scores.

    Args:
        scores (Dict[Tuple[str, str], int]): A dictionary of pairwise scores, where keys are
                                              sorted tuples of species names.
        output_filepath (str): The full path to the output JSON file.

    Raises:
        IOError: If there's an error writing to the file.
    """
    output_data: Dict[str, int] = {}
    for (s1, s2), score in scores.items():
        output_data[f"{s1}_{s2}"] = score

    try:
        output_dir = os.path.dirname(output_filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nSuccessfully saved pairwise scores to: {output_filepath}")
    except IOError as e:
        print(f"Error saving scores to file {output_filepath}: {e}")
        raise

def load_thresholds(filepath: str) -> List[float]:
    """
    Loads clustering thresholds from a text file, one float value per line.

    Args:
        filepath (str): The path to the thresholds text file.

    Returns:
        List[float]: A list of numerical thresholds.

    Raises:
        FileNotFoundError: If the thresholds file does not exist.
        ValueError: If any line in the file cannot be converted to a float.
        IOError: For other file reading errors.
    """
    thresholds = []
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Thresholds file not found at: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                stripped_line = line.strip()
                if not stripped_line:
                    continue
                try:
                    thresholds.append(float(stripped_line))
                except ValueError as e:
                    raise ValueError(
                        f"Invalid threshold value '{stripped_line}' on line {line_num} "
                        f"in file {filepath}. Must be a number."
                    ) from e
    except IOError as e:
        print(f"Error reading thresholds file {filepath}: {e}")
        raise
    return thresholds

def save_newick_tree(newick_string: str, output_filepath: str) -> None:
    """
    Saves a Newick string to a file.

    Args:
        newick_string (str): The Newick string to save.
        output_filepath (str): The full path to the output file.

    Raises:
        IOError: If there's an error writing to the file.
    """
    try:
        output_dir = os.path.dirname(output_filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_filepath, 'w', encoding='utf-8') as f:
            f.write(newick_string + ";\n")
        print(f"Successfully saved Newick tree to: {output_filepath}")
    except IOError as e:
        print(f"Error saving Newick tree to file {output_filepath}: {e}")
        raise

def save_clusters(
    clusters_data: Dict[str, List[List[str]]],
    output_filepath: str
) -> None:
    """
    Saves the calculated clusters for various thresholds to a JSON file.

    Args:
        clusters_data (Dict[str, List[List[str]]]): A dictionary where keys are string
                                                     representations of thresholds and values
                                                     are lists of clusters (each cluster is a list of species names).
        output_filepath (str): The full path to the output JSON file.

    Raises:
        IOError: If there's an error writing to the file.
    """
    try:
        output_dir = os.path.dirname(output_filepath)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(clusters_data, f, indent=2)
        print(f"\nSuccessfully saved clusters to: {output_filepath}")
    except IOError as e:
        print(f"Error saving clusters to file {output_filepath}: {e}")
        raise