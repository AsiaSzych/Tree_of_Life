# Phylogenetic Tree Builder

This Java 21 project builds a phylogenetic tree from amino acid sequences using the Needleman-Wunsch algorithm with a customizable BLOSUM matrix. It outputs similarity scores, a tree in Newick format, a dendrogram PNG, and clusters based on user-defined thresholds.

## Requirements

- Java 21
- Maven 3.9

## Setup

1. Clone the repository.
2. Place your input files (`organisms.json`, `blosumXX.json`, `thresholds.txt`) in the project root.
3. Build the project:

   ```sh
   mvn clean package
   ```

4. Run the program:

   ```sh
   java -jar target/phylo-1.0-SNAPSHOT.jar organisms.json blosumXX.json
   ```

## Input Files

- `organisms.json`: JSON mapping species names to amino acid sequences.
- `blosumXX.json`: JSON mapping for BLOSUM substitution matrix (XX = 50 or 62).
- `thresholds.txt`: One integer threshold per line.

## Output Files

- `organisms_scores_blosumXX.json`: Pairwise similarity scores.
- `tree_blosumXX_newick.nw`: Tree in Newick format (leaf names only).
- `tree_blosumXX_newick_with_distance.nw`: Tree in Newick format with branch lengths.
- `phylogenetic_tree_blosumXX.png`: Dendrogram image.
- `clusters_for_blosumXX.json`: Clusters for each threshold.

## Project Structure

- `src/main/java/com/example/phylo/`: All Java source files.
- `pom.xml`: Maven build file.

## License

MIT License

