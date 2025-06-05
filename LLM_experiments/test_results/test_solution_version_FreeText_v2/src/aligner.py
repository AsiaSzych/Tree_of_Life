# src/aligner.py
import numpy as np
from typing import Dict, Tuple
from collections import defaultdict

from src.utils import load_json_data

class NeedlemanWunschAligner:
    """
    A class to perform Needleman-Wunsch global sequence alignment.

    It uses a custom BLOSUM-like matrix for substitution and gap penalties.
    """

    def __init__(self, blosum_matrix_path: str):
        """
        Initializes the aligner by loading and parsing the BLOSUM-like matrix.

        Args:
            blosum_matrix_path (str): Path to the BLOSUM-like JSON file.
                                      Keys are single characters for gap penalties
                                      or two characters for substitution scores.
                                      Values are numerical scores.

        Raises:
            ValueError: If the BLOSUM matrix is invalid or incomplete.
        """
        self.blosum_matrix_path = blosum_matrix_path
        self._substitution_scores: Dict[Tuple[str, str], int] = {}
        self._gap_penalties: Dict[str, int] = {}
        self._alphabet: set[str] = set()

        self._load_and_parse_blosum_matrix()

    def _load_and_parse_blosum_matrix(self) -> None:
        """
        Loads the BLOSUM-like matrix from the specified path and parses it
        into internal substitution scores and gap penalties.
        """
        blosum_data = load_json_data(self.blosum_matrix_path)

        if not isinstance(blosum_data, dict):
            raise ValueError(
                f"Invalid BLOSUM matrix format in '{self.blosum_matrix_path}': "
                "Expected a dictionary."
            )

        for key, value in blosum_data.items():
            if not isinstance(value, (int, float)):
                raise ValueError(
                    f"Invalid score type for key '{key}' in '{self.blosum_matrix_path}': "
                    "Expected a number."
                )

            if len(key) == 1:
                # Single character key for gap penalty
                char = key.upper() # Normalize to uppercase for consistency
                self._gap_penalties[char] = int(value)
                self._alphabet.add(char)
            elif len(key) == 2:
                # Two character key for substitution score
                char1, char2 = key[0].upper(), key[1].upper() # Normalize to uppercase
                self._substitution_scores[(char1, char2)] = int(value)
                self._alphabet.add(char1)
                self._alphabet.add(char2)
            else:
                raise ValueError(
                    f"Invalid key format '{key}' in '{self.blosum_matrix_path}': "
                    "Keys must be 1 or 2 characters long."
                )

        if not self._alphabet:
            raise ValueError(
                f"BLOSUM matrix '{self.blosum_matrix_path}' is empty or contains no valid entries."
            )
        if not self._gap_penalties:
            # This check ensures that at least some gap penalties are defined,
            # which is crucial for the algorithm.
            raise ValueError(
                f"BLOSUM matrix '{self.blosum_matrix_path}' must define gap penalties "
                "for all characters in the alphabet (e.g., 'A': -X)."
            )

    def _get_score(self, char1: str, char2: str) -> int:
        """
        Retrieves the substitution score for two characters.

        Args:
            char1 (str): The first character.
            char2 (str): The second character.

        Returns:
            int: The substitution score.

        Raises:
            ValueError: If a character is not found in the defined alphabet
                        or if its substitution score is not defined.
        """
        char1_upper, char2_upper = char1.upper(), char2.upper()

        if char1_upper not in self._alphabet or char2_upper not in self._alphabet:
            raise ValueError(
                f"Character(s) '{char1}{char2}' not found in the BLOSUM matrix alphabet. "
                "Ensure all DNA bases (A, T, C, G) are defined."
            )

        # Check for direct match (e.g., "AA")
        score = self._substitution_scores.get((char1_upper, char2_upper))
        if score is not None:
            return score
        
        # Check for reverse match (e.g., "BA" if "AB" was not found)
        score = self._substitution_scores.get((char2_upper, char1_upper))
        if score is not None:
            return score

        raise ValueError(
            f"Substitution score for '{char1_upper}{char2_upper}' not defined "
            f"in '{self.blosum_matrix_path}'."
        )

    def _get_gap_penalty(self, char: str) -> int:
        """
        Retrieves the gap penalty for a single character.

        Args:
            char (str): The character for which to get the gap penalty.

        Returns:
            int: The gap penalty.

        Raises:
            ValueError: If the character's gap penalty is not defined.
        """
        char_upper = char.upper()
        penalty = self._gap_penalties.get(char_upper)
        if penalty is None:
            raise ValueError(
                f"Gap penalty for character '{char_upper}' not defined "
                f"in '{self.blosum_matrix_path}'."
            )
        return penalty

    def align(self, seq1: str, seq2: str) -> int:
        """
        Calculates the Needleman-Wunsch global alignment score between two sequences.

        Args:
            seq1 (str): The first DNA sequence.
            seq2 (str): The second DNA sequence.

        Returns:
            int: The optimal global alignment score.

        Raises:
            ValueError: If sequences contain characters not defined in the BLOSUM matrix.
        """
        if not seq1 or not seq2:
            # Handle empty sequences gracefully, though NW is typically for non-empty.
            # An empty sequence aligned with another usually results in cumulative gap penalties.
            # For simplicity, let's return 0 if either is empty, or handle as full gap cost.
            # For this problem, assuming non-empty sequences.
            if not seq1 and not seq2:
                return 0
            elif not seq1:
                return sum(self._get_gap_penalty(char) for char in seq2)
            else: # not seq2
                return sum(self._get_gap_penalty(char) for char in seq1)


        n = len(seq1)
        m = len(seq2)

        # Initialize the DP matrix with zeros
        # Using numpy for potentially better performance with large matrices
        dp_matrix = np.zeros((n + 1, m + 1), dtype=int)

        # Initialize the first row and column with gap penalties
        for i in range(1, n + 1):
            dp_matrix[i][0] = dp_matrix[i - 1][0] + self._get_gap_penalty(seq1[i - 1])
        for j in range(1, m + 1):
            dp_matrix[0][j] = dp_matrix[0][j - 1] + self._get_gap_penalty(seq2[j - 1])

        # Fill the DP matrix
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                # Match/Mismatch score
                match_score = dp_matrix[i - 1][j - 1] + self._get_score(seq1[i - 1], seq2[j - 1])

                # Gap in seq1 (deletion)
                delete_score = dp_matrix[i - 1][j] + self._get_gap_penalty(seq1[i - 1])

                # Gap in seq2 (insertion)
                insert_score = dp_matrix[i][j - 1] + self._get_gap_penalty(seq2[j - 1])

                dp_matrix[i][j] = max(match_score, delete_score, insert_score)

        return dp_matrix[n][m]
