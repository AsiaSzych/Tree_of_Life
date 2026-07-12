# Phylogenetic Clustering and Tree Visualization

This project computes pairwise similarity scores between species based on their amino acid sequences using the Needleman-Wunsch algorithm and a customizable BLOSUM matrix. It builds a phylogenetic tree, exports it in Newick format, draws a dendrogram, and clusters species based on user-defined thresholds.

## Requirements

- Java 21
- Maven 3.9+
- No external dependencies except Jackson for JSON parsing

## Setup

1. Clone the repository.
2. Place your input files (`organisms.json`, `blosumXX.json`, `thresholds.txt`) in the root directory.
3. Build the project:

   ```sh
   mvn clean package
   ```

4. Run the program:

   ```sh
   java -jar target/phylo-1.0-SNAPSHOT.jar organisms.json blosumXX.json
   ```

## Input Files

- `organisms.json`: Species names as keys, amino acid sequences as values.
- `blosumXX.json`: BLOSUM substitution matrix (e.g., blosum50.json or blosum62.json).
- `thresholds.txt`: One integer threshold per line.

## Output Files

- `organisms_scores_blosumXX.json`: Pairwise similarity scores.
- `tree_blosumXX_newick.nw`: Newick format (leaves only).
- `tree_blosumXX_newick_with_distance.nw`: Newick format (with branch distances).
- `phylogenetic_tree_blosumXX.png`: Dendrogram image.
- `clusters_for_blosumXX.json`: Clusters for each threshold.

## Project Structure

- `src/main/java/com/example/phylo/`: Java source code.
- `pom.xml`: Maven build file.

## License

MIT License