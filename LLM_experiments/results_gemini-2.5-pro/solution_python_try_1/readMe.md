# Phylogenetic Analysis Pipeline

This project implements a complete bioinformatics pipeline to perform phylogenetic analysis on a set of biological sequences. It calculates pairwise sequence similarity using the Needleman-Wunsch algorithm, constructs a phylogenetic tree via hierarchical clustering, visualizes the tree as a dendrogram, and finally, extracts distinct species clusters based on user-defined similarity thresholds.

## Features

-   **Pairwise Alignment:** Calculates similarity scores for all unique pairs of sequences using the Needleman-Wunsch algorithm.
-   **Custom Scoring:** Supports custom scoring matrices (e.g., BLOSUM50, BLOSUM62) provided in a simple JSON format.
-   **Hierarchical Clustering:** Builds a phylogenetic tree using the single-linkage agglomerative clustering method.
-   **Dendrogram Visualization:** Generates a clean, horizontal dendrogram where the x-axis represents the raw Needleman-Wunsch similarity score.
-   **Newick Format Export:** Saves the constructed tree in the standard Newick format, both with and without branch lengths.
-   **Threshold-based Clustering:** Extracts and reports flat clusters of species by "cutting" the tree at specified similarity thresholds.
-   **Modular Codebase:** The project is organized into logical modules for alignment, clustering, and visualization, making it easy to understand and extend.

## Project Structure

```
phylogenetic_pipeline/
├── data/
│   ├── organisms.json
│   ├── blosum50.json
│   ├── blosum62.json
│   └── thresholds.txt
├── results/
│   └── (This directory is created automatically by the script)
├── src/
│   ├── __init__.py
│   ├── alignment.py
│   ├── clustering.py
│   └── visualization.py
├── main.py
├── requirements.txt
└── README.md
```

## Prerequisites

-   Python 3.11 or newer
-   `pip` for package installation

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd phylogenetic_pipeline
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare your data:**
    -   Ensure your input files (`organisms.json`, `blosum50.json`, `blosum62.json`, and `thresholds.txt`) are placed in the `data/` directory.
    -   The script also requires a pre-calculated scores file (e.g., `organisms_scores_blosum50.json`). If this file does not exist, you will need to run a script that uses the `src/alignment.py` module to generate it first.

## How to Run

The main script orchestrates the tree-building, visualization, and cluster extraction parts of the pipeline, assuming the pairwise scores have already been calculated and saved.

1.  **Configure the run:**
    -   Open `main.py`.
    -   Locate the `BLOSUM_VERSION` variable and set it to the desired version you want to process (e.g., `"blosum50"` or `"blosum62"`). This will determine which score file is used as input.

    ```python
    # --- CHOOSE YOUR BLOSUM VERSION HERE ---
    BLOSUM_VERSION = "blosum50"
    # -----------------------------------------
    ```

2.  **Execute the script:**
    -   Run the main script from the project's root directory:
    ```bash
    python main.py
    ```

## Output

The script will print its progress and final cluster analysis to the console. It will also generate the following files in the `results/` directory:

-   `phylogenetic_tree_[version].png`: A PNG image of the horizontal dendrogram.
-   `tree_[version]_newick.nw`: The tree structure in Newick format without branch lengths.
-   `tree_[version]_newick_with_distance.nw`: The tree structure in Newick format with integer branch lengths.
-   `clusters_for_[version].json`: A JSON file containing the species clusters for each threshold specified in `thresholds.txt`.
