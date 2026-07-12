"""
Example script showing how to load previously saved scores.
"""
from src.score_saver import ScoreSaver


def main():
    """Load and display saved scores."""
    # Load scores for BLOSUM62
    try:
        scores = ScoreSaver.load_scores(blosum_type=62)
        print(f"Loaded {len(scores)} scores from BLOSUM62 results")
        
        # Show first 5 scores
        print("\nFirst 5 scores:")
        for i, (pair, score) in enumerate(scores.items()):
            if i >= 5:
                break
            print(f"  {pair}: {score}")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please run the main program first to generate scores.")


if __name__ == "__main__":
    main()