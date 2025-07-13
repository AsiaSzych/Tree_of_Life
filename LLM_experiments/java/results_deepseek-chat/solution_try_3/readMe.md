# Phylogenetic Analysis Pipeline

## Description
Java-based pipeline for:
1. Protein sequence alignment (Needleman-Wunsch)
2. Phylogenetic tree construction
3. Threshold-based clustering

## Requirements
- Java 21
- Maven 3.9+

## Input Files
Place these in `data/` directory:
- `organisms.json`: Species and sequences
- `blosumXX.json`: Scoring matrices
- `thresholds.txt`: Cluster thresholds

## Usage
```bash
mvn clean package
java -jar target/sequence-alignment-1.0-SNAPSHOT.jar \
  data/organisms.json data/blosum50.json data/thresholds.txt
```

## Output Files
- `organisms_scores_blosumXX.json`: Alignment scores
- `tree_blosumXX_*.nw`: Newick format trees
- `phylogenetic_tree_blosumXX.png`: Dendrogram
- `clusters_for_blosumXX.json`: Threshold clusters

## Example
```json
// organisms.json
{"Human": "MTA...", "Chimp": "MTA..."}

// thresholds.txt
1200
1100
```