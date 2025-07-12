"""Main entry point for phylogenetic clustering analysis."""

import sys
from src.main_complete_pipeline import main

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)