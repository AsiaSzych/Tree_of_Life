# Phylogenetic Analysis Pipeline

## Description
Tool for building phylogenetic trees from amino acid sequences using:
1. Needleman-Wunsch alignment
2. Single-linkage hierarchical clustering
3. Threshold-based species clustering

## Usage
```bash
python main.py organisms.json blosumXX.json thresholds.txt
```

## Output Files
- `output/organisms_scores_blosumXX.json`
- `output/tree_blosumXX_*.nw` (Newick formats)
- `output/phylogenetic_tree_blosumXX.png`
- `output/clusters_for_blosumXX.json`

## Input Examples
See `data/` directory for sample files.