"""
Test module for Needleman-Wunsch implementation.
"""
import json
from pathlib import Path
from .needleman_wunsch import NeedlemanWunsch, calculate_all_pairwise_scores


def test_needleman_wunsch():
    """Test the Needleman-Wunsch implementation with the provided example."""
    # Create test data directory
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)
    
    # Create test organisms file
    test_organisms = {
        "testspecies1": "aabaab",
        "testspecies2": "ababaa"
    }
    
    with open(test_dir / "test_organisms.json", 'w') as f:
        json.dump(test_organisms, f)
    
    # Create test BLOSUM file
    test_blosum = {
        "a": -1,
        "b": -2,
        "ab": -3,
        "ba": -3,
        "aa": 2,
        "bb": 3
    }
    
    with open(test_dir / "test_blosum.json", 'w') as f:
        json.dump(test_blosum, f)
    
    # Run alignment
    aligner = NeedlemanWunsch(str(test_dir / "test_blosum.json"))
    score = aligner.align("aabaab", "ababaa")
    
    print(f"Test alignment score: {score}")
    print(f"Expected score: 7")
    assert score == 7, f"Expected score 7, but got {score}"
    
    # Test all pairwise scores
    scores = calculate_all_pairwise_scores(
        test_organisms, 
        str(test_dir / "test_blosum.json")
    )
    
    print("\nAll pairwise scores:")
    for (sp1, sp2), score in scores.items():
        print(f"{sp1} vs {sp2}: {score}")
    
    # Clean up
    import shutil
    shutil.rmtree(test_dir)
    
    print("\nTest passed!")


if __name__ == "__main__":
    test_needleman_wunsch()