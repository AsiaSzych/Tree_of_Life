"""Main script to run the complete phylogenetic analysis pipeline."""

import logging
import argparse
from pathlib import Path

from .sequence_aligner import SequenceAligner
from .phylogenetic_tree import PhylogeneticTree
from .dendrogram import create_dendrogram
from .cluster_analyzer import ClusterAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run complete phylogenetic analysis pipeline."""
    parser = argparse.ArgumentParser(
        description="Complete phylogenetic analysis pipeline"
    )
    parser.add_argument(
        "--blosum",
        type=int,
        choices=[50, 62],
        default=62,
        help="BLOSUM matrix type (50 or 62)"
    )
    parser.add_argument(
        "--skip-alignment",
        action="store_true",
        help="Skip alignment calculation (use existing scores)"
    )
    parser.add_argument(
        "--skip-tree",
        action="store_true",
        help="Skip tree building (use existing tree)"
    )
    parser.add_argument(
        "--skip-dendrogram",
        action="store_true",
        help="Skip dendrogram creation"
    )
    parser.add_argument(
        "--thresholds-file",
        type=Path,
        default=Path("thresholds.txt"),
        help="Path to thresholds file"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("."),
        help="Output directory for all files"
    )
    
    args = parser.parse_args()
    
    try:
        scores_file = f"organisms_scores_blosum{args.blosum}.json"
        
        # Step 1: Calculate alignments (if not skipped)
        if not args.skip_alignment:
            logger.info("Step 1: Calculating sequence alignments...")
            aligner = SequenceAligner(blosum_type=args.blosum, base_path=args.output_dir)
            aligner.load_data()
            scores = aligner.calculate_all_alignments()
            aligner.save_scores()
        else:
            logger.info("Step 1: Skipped (using existing scores)")
            aligner = SequenceAligner(blosum_type=args.blosum, base_path=args.output_dir)
            scores = aligner.load_scores(scores_file)
        
        # Step 2: Build tree (if not skipped)
        if not args.skip_tree:
            logger.info("Step 2: Building phylogenetic tree...")
            tree = PhylogeneticTree(scores, blosum_type=args.blosum)
            tree.build_tree()
            tree.save_both_formats()
        else:
            logger.info("Step 2: Loading existing tree...")
            tree = PhylogeneticTree(scores, blosum_type=args.blosum)
            tree.build_tree()
        
        # Step 3: Create dendrogram (if not skipped)
        if not args.skip_dendrogram:
            logger.info("Step 3: Creating dendrogram...")
            create_dendrogram(tree, output_dir=args.output_dir)
        else:
            logger.info("Step 3: Skipped dendrogram creation")
        
        # Step 4: Analyze clusters
        logger.info("Step 4: Analyzing clusters...")
        analyzer = ClusterAnalyzer(tree)
        clusters = analyzer.run_analysis(
            thresholds_file=args.thresholds_file,
            output_file=args.output_dir / f"clusters_for_blosum{args.blosum}.json"
        )
        
        # Summary
        print(f"\n{'='*60}")
        print("Analysis Complete!")
        print(f"{'='*60}")
        print(f"BLOSUM type: {args.blosum}")
        print(f"Number of species: {len(tree._get_all_species())}")
        print(f"Number of thresholds analyzed: {len(clusters)}")
        print(f"Output directory: {args.output_dir}")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()