#!/bin/bash

# Build the project
echo "Building the project..."
mvn clean package

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "Running phylogenetic analysis..."
    
    # Run with default BLOSUM62 or with argument
    if [ $# -eq 0 ]; then
        java -jar target/phylogenetic-analysis-1.0.0.jar
    else
        java -jar target/phylogenetic-analysis-1.0.0.jar "$1"
    fi
else
    echo "Build failed!"
    exit 1
fi