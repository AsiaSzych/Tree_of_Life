# Phylogenetic Clustering Project

## Overview
This project implements a pipeline for:
1. Calculating protein sequence similarity using Needleman-Wunsch
2. Building phylogenetic trees
3. Generating clusters based on similarity thresholds
4. Visualizing evolutionary relationships

## Requirements
- Java 21
- Maven 3.9+

## Setup
```bash
git clone https://github.com/your-repo/phylogenetic-clustering.git
cd phylogenetic-clustering
mvn clean package
```

## Input Files
Place these in `data/input/`:
1. `organisms.json` - Species and their amino acid sequences
2. `blosumXX.json` - BLOSUM matrix (50 or 62)
3. `thresholds.txt` - Clustering thresholds (one per line)

## Execution Pipeline

### Step 1: Calculate Similarity Matrix
```bash
java -cp target/phylogenetic-clustering-1.0.0.jar \
  com.phylo.SimilarityMatrixCalculator \
  data/input/organisms.json \
  data/input/blosum50.json
```

### Step 2: Build Tree & Generate Outputs
```bash
java -cp target/phylogenetic-clustering-1.0.0.jar \
  com.phylo.TreeConstructionExecutor \
  data/output/organisms_scores_blosum50.json \
  data/input/organisms.json
```

## Output Files
Generated in `data/output/`:
1. `organisms_scores_blosumXX.json` - Pairwise similarity scores
2. `similarity_matrix.json` - Full similarity matrix
3. `tree_blosumXX_newick.nw` - Tree in Newick format
4. `tree_blosumXX_newick_with_distance.nw` - Newick with distances
5. `phylogenetic_tree_blosumXX.png` - Dendrogram visualization
6. `clusters_for_blosumXX.json` - Threshold-based clusters

## Project Structure
```
├── data
│   ├── input    # Input files
│   └── output   # Generated files
├── src          # Source code
└── target       # Build artifacts
```