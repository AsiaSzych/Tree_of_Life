# Phylogenetic Tree Builder

This project computes phylogenetic trees from amino acid sequences using the Needleman-Wunsch algorithm and BLOSUM substitution matrices. It outputs similarity scores, Newick tree files, dendrogram visualizations, and clusters based on user-defined thresholds.

## Setup

1. Install Python 3.11 (recommended: use `pyenv`).
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Input Files

- `organisms.json`: Dictionary mapping species names to amino acid sequences.
- `blosumXX.json`: BLOSUM substitution matrix (XX = 50 or 62).
- `thresholds.txt`: One integer threshold per line.

## Usage

1. Place your input files in the project directory.
2. Edit `main.py` to set the correct BLOSUM version (replace `XX`).
3. Run the program:
   ```
   python main.py
   ```

## Outputs

- `organisms_scores_blosumXX.json`: Pairwise similarity scores.
- `tree_blosumXX_newick.nw`: Newick tree (leaves only).
- `tree_blosumXX_newick_with_distance.nw`: Newick tree with branch lengths.
- `phylogenetic_tree_blosumXX.png`: Dendrogram visualization.
- `clusters_for_blosumXX.json`: Clusters for each threshold.

## License

MIT License