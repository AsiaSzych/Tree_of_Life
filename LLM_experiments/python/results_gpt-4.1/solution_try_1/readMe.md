# Phylogenetic Tree Construction and Clustering

This project computes pairwise Needleman-Wunsch similarity scores for amino acid sequences, builds a phylogenetic tree using single-linkage clustering, exports the tree in Newick format, draws a dendrogram, and finds clusters of species based on similarity thresholds.

## Setup

1. **Install Python 3.11** (recommended: use `pyenv`)
2. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

## Input Files

- `organisms.json`: Mapping of species names to amino acid sequences.
- `blosumXX.json`: BLOSUM substitution matrix (e.g., `blosum50.json` or `blosum62.json`).
- `thresholds.txt`: List of integer thresholds, one per line.

## Usage

1. Place your input files in the project directory.
2. Edit `main.py` to set the correct BLOSUM file (replace `blosumXX.json`).
3. Run the main script:
   ```
   python main.py
   ```

## Outputs

- Pairwise scores: `organisms_scores_blosumXX.json`
- Tree in Newick format: `tree_blosumXX_newick.nw`
- Tree in Newick format with distances: `tree_blosumXX_newick_with_distance.nw`
- Dendrogram image: `phylogenetic_tree_blosumXX.png`
- Clusters for thresholds: `clusters_for_blosumXX.json`

## File Descriptions

- `main.py`: Orchestrates the workflow.
- `needleman_wunsch.py`: Implements the Needleman-Wunsch algorithm.
- `tree.py`: Tree structure, clustering, Newick export, and threshold-based clustering.
- `dendrogram.py`: Dendrogram visualization.
