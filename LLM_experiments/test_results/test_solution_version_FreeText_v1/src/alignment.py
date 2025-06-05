# src/alignment.py

from typing import Dict, Tuple

def _parse_blosum_scores(blosum_data: Dict[str, int]) -> Tuple[Dict[Tuple[str, str], int], Dict[str, int]]:
    """
    Parses the raw BLOSUM-like dictionary into separate substitution and gap penalty matrices.

    Args:
        blosum_data (Dict[str, int]): The raw dictionary loaded from blosumXX.json.
                                      Keys are single characters (for gap penalties)
                                      or two concatenated characters (for substitution scores).

    Returns:
        Tuple[Dict[Tuple[str, str], int], Dict[str, int]]:
            - substitution_matrix (Dict[Tuple[str, str], int]): A dictionary where keys are
              tuples of (char1, char2) representing character pairs, and values are their
              substitution scores.
            - gap_penalties (Dict[str, int]): A dictionary where keys are single characters
              and values are their deletion costs.
    """
    substitution_matrix: Dict[Tuple[str, str], int] = {}
    gap_penalties: Dict[str, int] = {}

    for key, value in blosum_data.items():
        if len(key) == 1:
            # Single character key represents a gap penalty (deletion cost)
            gap_penalties[key] = value
        elif len(key) == 2:
            # Two character key represents a substitution score
            char1, char2 = key[0], key[1]
            substitution_matrix[(char1, char2)] = value
            # Assuming symmetry if not explicitly provided for both directions,
            # though the example implies both 'ab' and 'ba' will be present.
            if (char2, char1) not in substitution_matrix:
                substitution_matrix[(char2, char1)] = value
        else:
            # This case should ideally not happen with valid blosumXX.json
            print(f"Warning: Unexpected key format in BLOSUM data: '{key}'")

    return substitution_matrix, gap_penalties


def needleman_wunsch(
    seq1: str,
    seq2: str,
    substitution_matrix: Dict[Tuple[str, str], int],
    gap_penalties: Dict[str, int]
) -> int:
    """
    Calculates the Needleman-Wunsch global alignment similarity score between two sequences.

    Args:
        seq1 (str): The first DNA sequence.
        seq2 (str): The second DNA sequence.
        substitution_matrix (Dict[Tuple[str, str], int]): A dictionary defining scores
                                                          for matching/mismatching characters.
                                                          Keys are (char1, char2) tuples.
        gap_penalties (Dict[str, int]): A dictionary defining the cost of deleting
                                        each specific character. Keys are single characters.

    Returns:
        int: The maximum global alignment similarity score.

    Raises:
        ValueError: If a character in the sequences is not found in the gap_penalties
                    or substitution_matrix, indicating missing scoring information.
    """
    n = len(seq1)
    m = len(seq2)

    # Initialize the DP matrix
    # F[i][j] will store the maximum score for aligning seq1[:i] with seq2[:j]
    F = [[0] * (m + 1) for _ in range(n + 1)]

    # Initialize the first row and first column (gap penalties)
    for i in range(1, n + 1):
        char_in_seq1 = seq1[i - 1]
        if char_in_seq1 not in gap_penalties:
            raise ValueError(f"Missing gap penalty for character '{char_in_seq1}' in sequence 1.")
        F[i][0] = F[i - 1][0] + gap_penalties[char_in_seq1]

    for j in range(1, m + 1):
        char_in_seq2 = seq2[j - 1]
        if char_in_seq2 not in gap_penalties:
            raise ValueError(f"Missing gap penalty for character '{char_in_seq2}' in sequence 2.")
        F[0][j] = F[0][j - 1] + gap_penalties[char_in_seq2]

    # Fill the DP matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1 = seq1[i - 1]
            char2 = seq2[j - 1]

            # Score for match/mismatch
            # Use .get() with a default of -float('inf') to handle cases where a pair
            # might not be explicitly defined in the substitution matrix, though
            # the problem implies all necessary pairs will be present.
            match_mismatch_score = substitution_matrix.get(
                (char1, char2),
                substitution_matrix.get((char2, char1), -float('inf')) # Try symmetric key if direct not found
            )
            if match_mismatch_score == -float('inf'):
                 raise ValueError(f"Missing substitution score for pair ('{char1}', '{char2}').")

            score_match = F[i - 1][j - 1] + match_mismatch_score

            # Score for deletion (gap in seq2)
            if char1 not in gap_penalties:
                raise ValueError(f"Missing gap penalty for character '{char1}' in sequence 1.")
            score_delete = F[i - 1][j] + gap_penalties[char1]

            # Score for insertion (gap in seq1)
            if char2 not in gap_penalties:
                raise ValueError(f"Missing gap penalty for character '{char2}' in sequence 2.")
            score_insert = F[i][j - 1] + gap_penalties[char2]

            F[i][j] = max(score_match, score_delete, score_insert)

    return F[n][m]


def calculate_all_pairwise_scores(
    organisms_data: Dict[str, str],
    blosum_data: Dict[str, int]
) -> Dict[str, Dict[str, int]]:
    """
    Calculates Needleman-Wunsch similarity scores for all unique pairs of species.

    Args:
        organisms_data (Dict[str, str]): A dictionary where keys are species names
                                         and values are their DNA sequences.
        blosum_data (Dict[str, int]): The raw dictionary loaded from blosumXX.json.

    Returns:
        Dict[str, Dict[str, int]]: A nested dictionary where scores[species1][species2]
                                   gives the NW similarity score between species1 and species2.
                                   The matrix is symmetric.
    """
    substitution_matrix, gap_penalties = _parse_blosum_scores(blosum_data)

    species_names = list(organisms_data.keys())
    num_species = len(species_names)
    pairwise_scores: Dict[str, Dict[str, int]] = {name: {} for name in species_names}

    # Calculate scores for all unique pairs (including self-alignment)
    for i in range(num_species):
        species1_name = species_names[i]
        seq1 = organisms_data[species1_name]

        for j in range(i, num_species): # Start from 'i' to avoid redundant calculations
            species2_name = species_names[j]
            seq2 = organisms_data[species2_name]

            # Calculate NW score
            score = needleman_wunsch(seq1, seq2, substitution_matrix, gap_penalties)

            # Store the score symmetrically for fast access
            pairwise_scores[species1_name][species2_name] = score
            if species1_name != species2_name:
                pairwise_scores[species2_name][species1_name] = score

    return pairwise_scores