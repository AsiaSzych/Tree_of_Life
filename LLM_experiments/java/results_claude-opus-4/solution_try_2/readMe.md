# Phylogenetic Analysis Tool

A Java-based bioinformatics application for phylogenetic analysis of amino acid sequences using the Needleman-Wunsch algorithm and hierarchical clustering.

## Features

- **Sequence Alignment**: Calculates pairwise similarity scores using the Needleman-Wunsch algorithm
- **Phylogenetic Tree Construction**: Builds trees using agglomerative hierarchical clustering with single linkage
- **Visualization**: Generates dendrograms showing evolutionary relationships
- **Clustering**: Identifies species clusters based on similarity thresholds
- **Multiple Output Formats**: Supports Newick format export and JSON results

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

## Input Files

The application requires the following input files in the project root directory:

1. **organisms.json**: Species names and their amino acid sequences
```json
{
  "Species1": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
  "Species2": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
}
```

2. **blosumXX.json**: BLOSUM substitution matrix (where XX is 50 or 62)
```json
{
  "a": -1,
  "b": -2,
  "ab": -3,
  "aa": 2,
  "bb": 3
}
```

3. **thresholds.txt**: Threshold values for clustering (one per line)
```
1260
1150
980
```

## Usage

Run the application with default BLOSUM62 matrix:
```bash
java -jar target/phylogenetic-analysis-1.0.0.jar
```

Run with BLOSUM50 matrix:
```bash
java -jar target/phylogenetic-analysis-1.0.0.jar blosum50.json
```

## Output Files

The application generates the following output files:

1. **organisms_scores_blosumXX.json**: Pairwise alignment scores
2. **tree_blosumXX_newick.nw**: Phylogenetic tree in simple Newick format
3. **tree_blosumXX_newick_with_distance.nw**: Newick format with branch lengths
4. **phylogenetic_tree_blosumXX.png**: Dendrogram visualization
5. **clusters_for_blosumXX.json**: Clustering results for each threshold

## Algorithm Details

### Needleman-Wunsch Algorithm
- Global sequence alignment with affine gap penalties
- Uses BLOSUM substitution matrices for scoring
- Single character keys represent gap penalties
- Two character keys represent substitution scores

### Tree Construction
- Agglomerative hierarchical clustering
- Single linkage (maximum similarity between clusters)
- Tree height represents Needleman-Wunsch similarity scores

### Clustering
- Cuts tree at specified similarity thresholds
- Higher thresholds produce more, smaller clusters
- Lower thresholds produce fewer, larger clusters

## Development

### Project Structure
```
src/main/java/com/phylogenetic/
├── Main.java                 # Application entry point
├── model/                    # Data models
├── io/                       # File I/O operations
├── alignment/                # Sequence alignment algorithms
├── tree/                     # Tree construction and manipulation
├── clustering/               # Clustering algorithms
└── visualization/            # Dendrogram generation
```

### Running Tests
```bash
mvn test
```

### Code Style
This project follows the Google Java Style Guide with 2-space indentation.

## License

[Add your license information here]

## Authors

[Add author information here]