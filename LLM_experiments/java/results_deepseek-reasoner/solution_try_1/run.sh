#!/bin/bash

source "$HOME/.sdkman/bin/sdkman-init.sh"

# Configuration
BLOSUM_VERSION="62"  # Change to 62 for BLOSUM62
INPUT_DIR="data/input"
OUTPUT_DIR="data/output"

# Step 1: Calculate similarity scores
# java -cp target/phylogenetic-clustering-1.0.0-jar-with-dependencies.jar \
#   com.phylo.SimilarityMatrixCalculator \
#   $INPUT_DIR/organisms.json \
#   $INPUT_DIR/blosum$BLOSUM_VERSION.json

Step 2: Build phylogenetic tree and generate outputs
java -cp target/phylogenetic-clustering-1.0.0-jar-with-dependencies.jar \
  com.phylo.TreeConstructionExecutor \
  $OUTPUT_DIR/organisms_scores_blosum$BLOSUM_VERSION.json \
  $INPUT_DIR/organisms.json

echo "Pipeline executed successfully"