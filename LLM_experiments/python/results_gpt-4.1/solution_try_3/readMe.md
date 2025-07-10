# Phylogenetic Tree Construction and Clustering

## Overview

This project computes pairwise similarity scores between species using the Needleman-Wunsch algorithm with a custom BLOSUM matrix, builds a phylogenetic tree, exports it in Newick format, draws a dendrogram, and finds clusters of species based on similarity thresholds.

## Setup

1. **Python Version:**  
   Ensure you are using Python 3.11 (recommended: use `pyenv`).

2. **Install dependencies:**  
   ```
   pip install -r requirements.txt
   ```

3. **Prepare input files:**  
   Place your input files in the `data/` directory:
   - `organisms.json` (species and sequences)
   - `blosum50.json` or `blosum62.json` (BLOSUM matrix)
   - `thresholds.txt` (one integer threshold per line)