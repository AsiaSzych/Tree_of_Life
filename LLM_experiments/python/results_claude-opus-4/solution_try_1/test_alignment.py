"""
Test script to verify the Needleman-Wunsch implementation.
"""
import json
from src.sequence_alignment import NeedlemanWunsch


def test_example_case():
    """Test the provided example case."""
    # Create test data
    test_blosum = {
        "a": -1,
        "b": -2,
        "ab": -3,
        "ba": -3,
        "aa": 2,
        "bb": 3
    }
    
    # Create test sequences
    seq1 = "aabaab"  # testspecies1
    seq2 = "ababaa"  # testspecies2
    
    # Run alignment
    aligner = NeedlemanWunsch(test_blosum)
    score = aligner.align(seq1, seq2)
    
    print(f"Alignment score for '{seq1}' vs '{seq2}': {score}")
    print(f"Expected: 7")
    assert score == 7, f"Expected score 7, got {score}"
    print("Test passed!")


if __name__ == "__main__":
    test_example_case()