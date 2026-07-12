# Phylogenetic Clustering Pipeline

## Description
Tool for building phylogenetic trees from amino acid sequences using:
- Needleman-Wunsch alignment
- BLOSUM-based scoring
- Single-linkage clustering
- Threshold-based species grouping

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Prepare input files in `data/`:
   - `organisms.json`
   - `blosum50.json` or `blosum62.json`
   - `thresholds.txt`
3. Run analysis:
   ```bash
   python main.py --blosum 50
   ```

## Output Files
- `organisms_scores_blosumXX.json`
- `tree_blosumXX_newick.nw`
- `tree_blosumXX_newick_with_distance.nw`
- `phylogenetic_tree_blosumXX.png`
- `clusters_for_blosumXX.json`
