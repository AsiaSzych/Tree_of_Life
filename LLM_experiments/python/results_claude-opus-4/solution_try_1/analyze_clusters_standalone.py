"""
Standalone script for cluster analysis from existing tree.
"""
import argparse
import logging

from src.cluster_analyzer import ClusterAnalyzer


def main():
    """Run cluster analysis on existing tree data."""
    parser = argparse.ArgumentParser(description="Analyze clusters from phylogenetic tree")
    parser.add_argument(
        "--blosum",
        type=int,
        choices=[50, 62],
        default=62,
        help="BLOSUM matrix type"
    )
    
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        analyzer = ClusterAnalyzer(blosum_type=args.blosum)
        clusters = analyzer.run_full_analysis()
        
        print(f"\nAnalysis complete. Results saved to clusters_for_blosum{args.blosum}.json")
        
    except Exception as e:
        logging.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()