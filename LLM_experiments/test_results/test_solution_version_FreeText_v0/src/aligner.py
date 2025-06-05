# src/aligner.py

import json
import os
from typing import Dict

class NeedlemanWunschAligner:
    """
    Calculates Needleman-Wunsch global alignment scores between DNA sequences
    based on a provided BLOSUM-like scoring matrix.

    The BLOSUM-like matrix defines:
    - Single-character keys (e.g., "A", "T"): Cost of deleting/inserting that character.
    - Two-character keys (e.g., "AA", "AT"): Cost of substituting one character for another.
    """

    def __init__(self, blosum_filepath: str):
        """
        Initializes the aligner with the specified BLOSUM scoring matrix.

        Args:
            blosum_filepath (str): Path to the BLOSUM JSON file.
        """
        self.blosum_costs = self._load_blosum_matrix(blosum_filepath)

    def _load_blosum_matrix(self, filepath: str) -> Dict[str, int]:
        """
        Loads the BLOSUM-like scoring matrix from a JSON file.

        Args:
            filepath (str): The path to the BLOSUM JSON file.

        Returns:
            Dict[str, int]: A dictionary representing the BLOSUM costs.

        Raises:
            FileNotFoundError: If the BLOSUM file does not exist.
            json.JSONDecodeError: If the BLOSUM file is not valid JSON.
            ValueError: If the BLOSUM file has an invalid structure or content.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"BLOSUM file not found at: {filepath}")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                blosum_data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Invalid JSON in BLOSUM file {filepath}: {e}", e.doc, e.pos)

        if not isinstance(blosum_data, dict):
            raise ValueError(f"BLOSUM file {filepath} must contain a JSON object (dictionary).")

        for key, value in blosum_data.items():
            if not isinstance(key, str) or not isinstance(value, (int, float)):
                raise ValueError(
                    f"BLOSUM file {filepath} contains invalid key-value pair: '{key}': {value}. "
                    "Keys must be strings, values must be numbers."
                )
            if not (1 <= len(key) <= 2):
                raise ValueError(
                    f"BLOSUM key '{key}' has invalid length ({len(key)}). "
                    "Keys must be 1 (for gap penalty) or 2 (for substitution) characters."
                )
        return blosum_data

    def _get_substitution_score(self, char1: str, char2: str) -> int:
        """
        Retrieves the substitution score for two characters from the BLOSUM matrix.
        Handles symmetric keys (e.g., "AB" or "BA").

        Args:
            char1 (str): The first character.
            char2 (str): The second character.

        Returns:
            int: The substitution score.

        Raises:
            KeyError: If the substitution score for the given characters is not found
                      in the loaded BLOSUM matrix.
        """
        key = char1 + char2
        if key in self.blosum_costs:
            return int(self.blosum_costs[key])

        reversed_key = char2 + char1
        if reversed_key in self.blosum_costs:
            return int(self.blosum_costs[reversed_key])

        raise KeyError(
            f"Substitution score for characters '{char1}' and '{char2}' not found in BLOSUM matrix. "
            f"Missing keys: '{key}' or '{reversed_key}'."
        )

    def _get_gap_penalty(self, char: str) -> int:
        """
        Retrieves the character-specific gap penalty from the BLOSUM matrix.

        Args:
            char (str): The character for which to get the gap penalty.

        Returns:
            int: The gap penalty.

        Raises:
            KeyError: If the gap penalty for the given character is not found
                      in the loaded BLOSUM matrix.
        """
        if char in self.blosum_costs:
            return int(self.blosum_costs[char])
        raise KeyError(f"Gap penalty for character '{char}' not found in BLOSUM matrix.")

    def align(self, seq1: str, seq2: str) -> int:
        """
        Calculates the Needleman-Wunsch global alignment score between two sequences.

        Args:
            seq1 (str): The first DNA sequence.
            seq2 (str): The second DNA sequence.

        Returns:
            int: The global alignment score.

        Raises:
            ValueError: If sequences contain characters not fully defined in the BLOSUM matrix
                        (missing substitution scores or gap penalties).
        """
        n = len(seq1)
        m = len(seq2)

        dp_matrix = [[0] * (m + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            try:
                dp_matrix[i][0] = dp_matrix[i-1][0] + self._get_gap_penalty(seq1[i-1])
            except KeyError as e:
                raise ValueError(
                    f"Character '{seq1[i-1]}' in sequence 1 (at index {i-1}) "
                    f"not found in BLOSUM for gap penalty: {e}"
                ) from e

        for j in range(1, m + 1):
            try:
                dp_matrix[0][j] = dp_matrix[0][j-1] + self._get_gap_penalty(seq2[j-1])
            except KeyError as e:
                raise ValueError(
                    f"Character '{seq2[j-1]}' in sequence 2 (at index {j-1}) "
                    f"not found in BLOSUM for gap penalty: {e}"
                ) from e

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                char1 = seq1[i-1]
                char2 = seq2[j-1]

                try:
                    score_match_mismatch = dp_matrix[i-1][j-1] + self._get_substitution_score(char1, char2)
                    score_delete_seq1 = dp_matrix[i][j-1] + self._get_gap_penalty(char2)
                    score_delete_seq2 = dp_matrix[i-1][j] + self._get_gap_penalty(char1)

                except KeyError as e:
                    raise ValueError(
                        f"Character(s) '{char1}' or '{char2}' not fully defined in BLOSUM matrix. "
                        f"Ensure all necessary substitution scores and gap penalties are present: {e}"
                    ) from e

                dp_matrix[i][j] = max(score_match_mismatch, score_delete_seq1, score_delete_seq2)

        return dp_matrix[n][m]
