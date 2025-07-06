# Phylogenetic Tree Builder

This project performs hierarchical clustering on a set of species based on their amino acid sequences. It is a complete, end-to-end pipeline written in Java 21 and built with Maven.

## Features

1.  **Pairwise Similarity Calculation:** Calculates similarity scores for all pairs of species using the Needleman-Wunsch algorithm and a configurable BLOSUM scoring matrix.
2.  **Phylogenetic Tree Construction:** Builds a hierarchical tree using an agglomerative clustering algorithm (single-linkage based on maximum similarity).
3.  **Results Export:**
    *   Saves the tree in standard Newick format (with and without branch lengths).
    *   Generates a visual dendrogram of the tree and saves it as a PNG image.
4.  **Threshold-Based Clustering:** Reads a list of similarity thresholds and identifies the resulting species clusters for each one, saving the output to a JSON file.

## Project Structure

- `pom.xml`: The Maven build file, containing all project dependencies.
- `data/`: Contains all input files.
  - `organisms.json`: A map of species names to their amino acid sequences.
  - `blosumXX.json`: The scoring matrix for the Needleman-Wunsch algorithm.
  - `thresholds.txt`: A list of integer thresholds for the final clustering step.
- `src/`: Contains all Java source code, organized by feature.
- `output/`: (Generated on run) Contains all output files, such as Newick trees, the dendrogram PNG, and the final cluster analysis JSON.

## How to Build and Run

### Prerequisites

- Java 21 (or later)
- Apache Maven 3.9 (or later)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd phylogenetic-tree-builder
    ```

2.  **Build the project:**
    Maven will download all necessary dependencies and compile the code into a single executable JAR file in the `target/` directory.
    ```bash
    mvn clean package
    ```

3.  **Run the application:**
    Execute the generated JAR file from the project's root directory. The program will read from the `data/` directory and write all results to a new `output/` directory.
    ```bash
    java -jar target/phylogenetic-tree-builder-1.0-SNAPSHOT.jar
    ```

The console will display the progress of the analysis, and all output files will be available in the `output/` folder upon completion.