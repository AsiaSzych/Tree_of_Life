# Phylogenetic Clustering Analysis

A Python implementation for phylogenetic analysis of amino acid sequences using Needleman-Wunsch alignment, hierarchical clustering, and threshold-based species grouping.

## Features

- **Sequence Alignment**: Needleman-Wunsch algorithm with BLOSUM scoring matrices
- **Phylogenetic Tree Construction**: Single-linkage hierarchical clustering
- **Visualization**: Horizontal dendrograms with similarity-based distances
- **Clustering**: Threshold-based species grouping
- **Multiple Output Formats**: JSON, Newick, and PNG visualizations

## Requirements

- Python 3.11+
- pyenv (recommended for environment management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phylogenetic-clustering
```

2. Create a Python environment using pyenv:
```bash
pyenv virtualenv 3.11.0 phylogenetic-env
pyenv activate phylogenetic-env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Input Files

The program requires the following input files in the project root:

1. **`organisms.json`**: Species and their amino acid sequences
   ```json
   {
     "Species1": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
     "Species2": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
   }
   ```

2. **`blosumXX.json`**: BLOSUM scoring matrix (XX = 50 or 62)
   ```json
   {
     "a": -1,
     "b": -2,
     "ab": -3,
     "aa": 2,
     "bb": 3
   }
   ```

3. **`thresholds.txt`**: Clustering thresholds (one per line)
   ```
   1260
   1150
   980
   ```

## Usage

### Basic Usage

Run the complete analysis with default BLOSUM62:
```bash
python main.py
```

Run with BLOSUM50:
```bash
python main.py blosum50.json
```

### Run Analysis for Both BLOSUM Matrices

```bash
python run_analysis.py
```

### Test Clustering Functionality

```bash
python test_clustering.py
```

## Output Files

The program generates the following output files:

1. **Alignment Scores**: `organisms_scores_blosumXX.json`
2. **Newick Formats**:
   - Simple: `tree_blosumXX_newick.nw`
   - With distances: `tree_blosumXX_newick_with_distance.nw`
3. **Dendrogram**: `phylogenetic_tree_blosumXX.png`
4. **Clusters**: `clusters_for_blosumXX.json`
5. **Analysis Plots**: `cluster_analysis_blosumXX.png`

## Project Structure

- `src/alignment/`: Needleman-Wunsch implementation
- `src/tree/`: Phylogenetic tree construction
- `src/visualization/`: Dendrogram generation
- `src/clustering/`: Threshold-based clustering

## Algorithm Details

### Needleman-Wunsch Alignment
- Global sequence alignment with affine gap penalties
- Scoring based on BLOSUM substitution matrices
- Returns integer similarity scores

### Tree Construction
- Single-linkage hierarchical clustering
- Uses similarity scores (not distances)
- Heights represent merge similarity values

### Clustering
- Cuts tree at specified thresholds
- Identifies connected components
- Groups species below threshold values

## License

[Your License Here]

## Author

[Your Name Here]