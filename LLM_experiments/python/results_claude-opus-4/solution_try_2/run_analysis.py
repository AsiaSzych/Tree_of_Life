"""
Utility script to run analysis with different BLOSUM matrices.
"""
from pathlib import Path
from src.alignment import (
    load_organisms,
    calculate_all_pairwise_scores,
    save_scores_to_json
)


def run_with_both_blosum_matrices():
    """Run the analysis with both BLOSUM50 and BLOSUM62 matrices."""
    organisms_file = "organisms.json"
    blosum_files = ["blosum50.json", "blosum62.json"]
    
    # Load organisms once
    print("Loading organisms...")
    organisms = load_organisms(organisms_file)
    
    for blosum_file in blosum_files:
        if not Path(blosum_file).exists():
            print(f"Skipping {blosum_file} - file not found")
            continue
            
        print(f"\n{'='*50}")
        print(f"Running analysis with {blosum_file}")
        print('='*50)
        
        # Calculate scores
        pairwise_scores = calculate_all_pairwise_scores(organisms, blosum_file)
        
        # Save results
        output_file = save_scores_to_json(pairwise_scores, blosum_file)
        print(f"Results saved to: {output_file}")
        
        # Show statistics
        unique_pairs = sum(1 for (s1, s2) in pairwise_scores.keys() if s1 < s2)
        print(f"Total unique pairs (excluding self): {unique_pairs}")


if __name__ == "__main__":
    run_with_both_blosum_matrices()