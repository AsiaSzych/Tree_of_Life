# Phylogenetic Tree Builder

This project constructs a phylogenetic tree from amino acid sequences using the Needleman-Wunsch algorithm and BLOSUM substitution matrices. It supports visualization, Newick export, and clustering based on similarity thresholds.

## Features

- Reads amino acid sequences (`organisms.json`) and BLOSUM matrix (`blosumXX.json`)
- Computes pairwise Needleman-Wunsch similarity scores
- Builds a phylogenetic tree using single-linkage clustering (on similarity)
- Exports tree in Newick format (with and without branch lengths)
- Draws a horizontal dendrogram (`phylogenetic_tree_blosumXX.png`)
- Extracts clusters for thresholds from `thresholds.txt`
- Saves all intermediate and final results to JSON files

## Requirements

- Java 21
- Maven 3.9+
- See `pom.xml` for dependencies

## Setup

1. Clone the repository.
2. Place your input files in the root directory:
   - `organisms.json`
   - `blosum50.json` or `blosum62.json`
   - `thresholds.txt`
3. Build the project:
   ```sh
   mvn clean package
   ```
4. Run the program:
   ```sh
   java -cp target/phylo-tree-1.0-SNAPSHOT.jar com.example.phylo.Main
   ```

## Output

- `organisms_scores_blosumXX.json`: Pairwise similarity scores
- `tree_blosumXX_newick.nw`: Newick format (simple)
- `tree_blosumXX_newick_with_distance.nw`: Newick format (with branch lengths)
- `phylogenetic_tree_blosumXX.png`: Dendrogram
- `clusters_for_blosumXX.json`: Clusters for each threshold

## License

MIT