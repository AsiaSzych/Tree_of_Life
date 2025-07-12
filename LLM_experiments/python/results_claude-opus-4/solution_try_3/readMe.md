# Phylogenetic Clustering Analysis

A Python implementation of phylogenetic tree construction and clustering analysis using Needleman-Wunsch sequence alignment.

## Features

- Needleman-Wunsch algorithm for amino acid sequence alignment
- Phylogenetic tree construction using single-linkage clustering
- Dendrogram visualization with similarity-based distances
- Threshold-based clustering analysis
- Support for BLOSUM50 and BLOSUM62 substitution matrices

## Requirements

- Python 3.11+
- See `requirements.txt` for package dependencies

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phylogenetic-clustering
```

2. Create a virtual environment using pyenv:
```bash
pyenv virtualenv 3.11.0 phylogenetic-env
pyenv activate phylogenetic-env
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install the package in development mode:
```bash
pip install -e .
```

## Input Files

The pipeline requires three input files:

1. **organisms.json**: Species names and amino acid sequences
   ```json
   {
     "Species1": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
     "Species2": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
   }
   ```

2. **blosumXX.json**: BLOSUM substitution matrix (XX = 50 or 62)
   ```json
   {
     "a": -1,
     "b": -2,
     "ab": -3,
     "aa": 2,
     "bb": 3
   }
   ```

3. **thresholds.txt**: Similarity thresholds for clustering (one per line)
   ```
   850
   920
   1050
   ```

## Usage

### Quick Start

Run the complete analysis pipeline:

```bash
python run_analysis.py --blosum 62
```

### Command Line Options

```bash
python run_analysis.py [OPTIONS]

Options:
  --blosum {50,62}      BLOSUM matrix type (default: 62)
  --skip-alignment      Skip alignment calculation (use existing scores)
  --skip-tree          Skip tree building
  --skip-dendrogram    Skip dendrogram creation
  --output-dir PATH    Output directory (default: current directory)
  --thresholds-file    Path to thresholds file (default: thresholds.txt)
```

### Step-by-Step Usage

1. **Calculate sequence alignments only:**
   ```python
   from src.sequence_aligner import SequenceAligner
   
   aligner = SequenceAligner(blosum_type=62)
   aligner.load_data()
   scores = aligner.calculate_all_alignments()
   aligner.save_scores()
   ```

2. **Build phylogenetic tree:**
   ```python
   from src.phylogenetic_tree import build_tree_from_scores
   
   tree = build_tree_from_scores("organisms_scores_blosum62.json")
   tree.save_both_formats()
   ```

3. **Generate clusters:**
   ```python
   from src.cluster_analyzer import analyze_clusters_from_tree
   
   clusters = analyze_clusters_from_tree(tree)
   ```

## Output Files

- `organisms_scores_blosumXX.json`: Pairwise alignment scores
- `tree_blosumXX_newick.nw`: Tree in simple Newick format
- `tree_blosumXX_newick_with_distance.nw`: Tree with branch lengths
- `phylogenetic_tree_blosumXX.png`: Dendrogram visualization
- `clusters_for_blosumXX.json`: Clustering results for each threshold

## Example

See `examples/` directory for sample data generation and usage examples.

## Project Structure

```
src/
├── data_loader.py          # Input file handling
├── needleman_wunsch.py     # Sequence alignment algorithm
├── sequence_aligner.py     # Pairwise alignment orchestration
├── tree_node.py           # Tree data structure
├── phylogenetic_tree.py   # Tree construction algorithm
├── dendrogram.py          # Tree visualization
├── cluster_analyzer.py    # Threshold-based clustering
└── main_complete_pipeline.py  # Complete pipeline implementation
```

## License

MIT License