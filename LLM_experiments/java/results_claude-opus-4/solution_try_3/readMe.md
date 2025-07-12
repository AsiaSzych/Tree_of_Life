# Phylogenetic Analysis Tool

A Java-based tool for phylogenetic analysis of amino acid sequences using the Needleman-Wunsch algorithm and hierarchical clustering.

## Features

- **Sequence Alignment**: Implements the Needleman-Wunsch algorithm for global sequence alignment
- **Phylogenetic Tree Construction**: Builds trees using single-linkage hierarchical clustering
- **Multiple Output Formats**: Exports trees in Newick format and generates dendrogram visualizations
- **Threshold-based Clustering**: Identifies species clusters at different similarity thresholds
- **BLOSUM Matrix Support**: Works with both BLOSUM50 and BLOSUM62 substitution matrices

## Requirements

- Java 21 or higher
- Maven 3.9 or higher

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd phylogenetic-analysis
```

2. Build the project:
```bash
mvn clean package
```

## Usage

### Basic Usage

Run with BLOSUM50 (default):
```bash
java -jar target/phylogenetic-analysis-1.0.0.jar
```

Run with BLOSUM62:
```bash
java -jar target/phylogenetic-analysis-1.0.0.jar 62
```

### Input Files

Place the following files in the project root directory:

1. **organisms.json** - Species and their amino acid sequences
```json
{
  "Species1": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
  "Species2": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
}
```

2. **blosum50.json** or **blosum62.json** - BLOSUM substitution matrix
```json
{
  "a": -1,
  "b": -2,
  "ab": -3,
  "aa": 2,
  "bb": 3
}
```

3. **thresholds.txt** (optional) - Clustering thresholds
```
1260
1150
980
```

### Output Files

The program generates the following output files:

- `organisms_scores_blosum{50|62}.json` - Pairwise alignment scores
- `tree_blosum{50|62}_newick.nw` - Tree in simple Newick format
- `tree_blosum{50|62}_newick_with_distance.nw` - Tree with branch distances
- `phylogenetic_tree_blosum{50|62}.png` - Dendrogram visualization
- `clusters_for_blosum{50|62}.json` - Clustering results (if thresholds.txt exists)

## Project Structure

```
src/main/java/com/phylogenetic/
├── Main.java                    # Application entry point
├── alignment/                   # Needleman-Wunsch implementation
├── clustering/                  # Threshold-based clustering
├── config/                      # Configuration classes
├── io/                         # File I/O operations
├── model/                      # Data models
├── tree/                       # Tree construction and manipulation
└── visualization/              # Dendrogram generation
```

## Algorithm Details

### Needleman-Wunsch Algorithm
- Global sequence alignment with affine gap penalties
- Uses BLOSUM substitution matrices for scoring
- Returns integer similarity scores

### Tree Construction
- Single-linkage hierarchical clustering
- Merges nodes with highest similarity first
- Preserves raw Needleman-Wunsch scores as branch heights

### Clustering
- Cuts tree at specified similarity thresholds
- Groups species that remain connected above threshold
- Outputs clusters as lists of species names

## Testing

Run unit tests:
```bash
mvn test
```

## License

[Your License Here]

## Authors

[Your Name Here]