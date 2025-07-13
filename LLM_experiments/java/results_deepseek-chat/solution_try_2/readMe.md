# Phylogenetic Analysis Tool

## Description
Java-based pipeline for:
1. Protein sequence alignment (Needleman-Wunsch)
2. Phylogenetic tree construction
3. Threshold-based clustering
4. Dendrogram visualization

## Requirements
- Java 21
- Maven 3.9+

## Usage
```bash
mvn compile exec:java -Dexec.args="62"  # Use BLOSUM62 matrix
```

## Input Files
- `data/organisms.json`: Species and their sequences
- `data/blosumXX.json`: Substitution matrices
- `data/thresholds.txt`: Clustering thresholds

## Output Files
- `organisms_scores_blosumXX.json`: Alignment scores
- `tree_blosumXX_*.nw`: Newick format trees
- `phylogenetic_tree_blosumXX.png`: Dendrogram
- `clusters_for_blosumXX.json`: Threshold clusters
