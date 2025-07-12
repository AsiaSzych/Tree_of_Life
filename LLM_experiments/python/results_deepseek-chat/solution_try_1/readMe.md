# Phylogenetic Clustering Pipeline

## Description
A Python pipeline for:
1. Calculating Needleman-Wunsch similarity scores for amino acid sequences
2. Building phylogenetic trees using single-linkage clustering
3. Identifying species clusters at specified similarity thresholds

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place input files in `data/`:
   - `organisms.json`
   - `blosum50.json` or `blosum62.json`
   - `thresholds.txt`
3. Run:
   ```bash
   python main.py
   ```

## Output Files
- `outputs/organisms_scores_blosumXX.json`: Pairwise NW scores
- `outputs/phylogenetic_tree_blosumXX.png`: Dendrogram visualization
- `outputs/clusters_for_blosumXX.json`: Threshold-based clusters