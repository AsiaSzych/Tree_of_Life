"""
Main entry point for the phylogenetic analysis project.
"""
import logging
import argparse
from pathlib import Path

from src.similarity_calculator import SimilarityCalculator


def setup_logging(level: str = "INFO"):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Main function to run the similarity calculation and tree building."""
    parser = argparse.ArgumentParser(description="Phylogenetic analysis pipeline")
    parser.add_argument(
        "--blosum", 
        type=int, 
        choices=[50, 62], 
        default=62,
        help="BLOSUM matrix type to use (50 or 62)"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save results to file"
    )
    parser.add_argument(
        "--build-tree",
        action="store_true",
        help="Build phylogenetic tree after calculating scores"
    )
    parser.add_argument(
        "--tree-only",
        action="store_true",
        help="Only build tree from existing scores file"
    )
    parser.add_argument(
        "--save-newick",
        action="store_true",
        help="Save tree in Newick formats"
    )
    parser.add_argument(
        "--draw-dendrogram",
        action="store_true",
        help="Draw and save dendrogram visualization"
    )
    parser.add_argument(
        "--analyze-clusters",
        action="store_true",
        help="Analyze clusters at thresholds from thresholds.txt"
    )
    parser.add_argument(
        "--full-pipeline",
        action="store_true",
        help="Run full pipeline: calculate scores, build tree, save formats, analyze clusters"
    )
    
    args = parser.parse_args()
    
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        calculator = SimilarityCalculator(blosum_type=args.blosum)
        tree = None
        
        # Handle full pipeline
        if args.full_pipeline:
            args.build_tree = True
            args.save_newick = True
            args.draw_dendrogram = True
            args.analyze_clusters = True
        
        if args.tree_only: #or args.analyze_clusters:
            # Only build tree from existing scores
            logger.info("Building tree from existing scores file")
            tree = calculator.build_phylogenetic_tree()
        else:
            # Calculate similarity scores
            scores = calculator.calculate_all_pairs(save_to_file=not args.no_save)
            
            logger.info("Similarity calculation completed successfully")
            logger.info(f"Total number of scores calculated: {len(scores)}")
            
            if not args.no_save:
                output_file = f"organisms_scores_blosum{args.blosum}.json"
                logger.info(f"Results saved to: {output_file}")
            
            # Build tree if needed
            if args.build_tree or args.save_newick or args.draw_dendrogram or args.analyze_clusters:
                logger.info("Building phylogenetic tree")
                tree = calculator.build_phylogenetic_tree(scores)
        
        # Process tree if built
        if tree and tree.root:
            logger.info("Tree construction successful")
            logger.info(f"Tree root height: {tree.root.height}")
            
            # Save Newick formats
            if args.save_newick:
                simple_path, distance_path = calculator.save_tree_newick(tree)
                logger.info(f"Saved Newick formats:")
                logger.info(f"  Simple: {simple_path}")
                logger.info(f"  With distances: {distance_path}")
            
            # Draw dendrogram
            if args.draw_dendrogram:
                dendrogram_path = calculator.draw_dendrogram(tree)
                logger.info(f"Saved dendrogram: {dendrogram_path}")
            
            # Analyze clusters
            if args.analyze_clusters:
                logger.info("Analyzing clusters at specified thresholds")
                clusters = calculator.analyze_clusters(tree)
                logger.info(f"Cluster analysis complete for {len(clusters)} thresholds")
            
    except Exception as e:
        logger.error(f"Error during execution: {e}")
        raise


if __name__ == "__main__":
    main()