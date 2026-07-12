# Phylogenetic Analysis Pipeline

A Python-based pipeline for phylogenetic analysis using Needleman-Wunsch sequence alignment, hierarchical clustering, and threshold-based species clustering.

## Features

- **Sequence Alignment**: Needleman-Wunsch algorithm with customizable BLOSUM matrices
- **Phylogenetic Tree Construction**: Single-linkage hierarchical clustering
- **Visualization**: Horizontal dendrograms with similarity-based distances
- **Clustering Analysis**: Threshold-based species clustering
- **Multiple Output Formats**: JSON, Newick, and PNG visualizations

## Requirements

- Python 3.11+
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phylogenetic-analysis
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Input Files

The pipeline requires the following input files in the project root:

1. **organisms.json**: Species names and amino acid sequences
   ```json
   {
     "Species1": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
     "Species2": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
   }
   ```

2. **blosum50.json** or **blosum62.json**: BLOSUM substitution matrices
   ```json
   {
     "A": -1,
     "AA": 4,
     "AC": 0,
     ...
   }
   ```

3. **thresholds.txt**: Clustering thresholds (one per line)
   ```
   1260
   1150
   980
   ```

## Usage

### Full Pipeline
Run the complete analysis pipeline:
```bash
python main.py --full-pipeline --blosum 62
```

### Individual Steps

1. **Calculate similarity scores only**:
   ```bash
   python main.py --blosum 62
   ```

2. **Build tree from existing scores**:
   ```bash
   python main.py --tree-only --blosum 62
   ```

3. **Generate all outputs**:
   ```bash
   python main.py --build-tree --save-newick --draw-dendrogram --analyze-clusters --blosum 62
   ```

4. **Analyze clusters only**:
   ```bash
   python analyze_clusters_standalone.py --blosum 62
   ```

### Command-line Options

- `--blosum {50,62}`: Choose BLOSUM matrix type (default: 62)
- `--log-level {DEBUG,INFO,WARNING,ERROR}`: Set logging level (default: INFO)
- `--no-save`: Don't save similarity scores to file
- `--build-tree`: Build phylogenetic tree after calculating scores
- `--tree-only`: Build tree from existing scores file
- `--save-newick`: Save tree in Newick formats
- `--draw-dendrogram`: Generate dendrogram visualization
- `--analyze-clusters`: Perform threshold-based clustering analysis
- `--full-pipeline`: Run all steps

## Output Files

The pipeline generates the following output files:

1. **organisms_scores_blosum{50,62}.json**: Pairwise similarity scores
2. **tree_blosum{50,62}_newick.nw**: Simple Newick format (topology only)
3. **tree_blosum{50,62}_newick_with_distance.nw**: Newick with branch lengths
4. **phylogenetic_tree_blosum{50,62}.png**: Dendrogram visualization
5. **clusters_for_blosum{50,62}.json**: Clustering results for all thresholds

## Testing

Run the test script to verify the Needleman-Wunsch implementation:
```bash
python test_alignment.py
```

## Example Workflow

```bash
# 1. Ensure input files are in place
ls organisms.json blosum62.json thresholds.txt

# 2. Run full analysis
python main.py --full-pipeline --blosum 62

# 3. View results
cat clusters_for_blosum62.json
```

## License

[Your License Here]

## Author

[Your Name Here]