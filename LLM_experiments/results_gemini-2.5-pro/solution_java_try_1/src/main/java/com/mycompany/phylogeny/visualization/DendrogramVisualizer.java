package com.mycompany.phylogeny.visualization;

import com.mycompany.phylogeny.algorithm.ClusteringResult;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import smile.plot.swing.Canvas;
import smile.plot.swing.Dendrogram;

/**
 * Creates and saves a visual dendrogram from clustering results.
 */
public class DendrogramVisualizer {

  /**
   * Generates a dendrogram and saves it to a PNG file.
   *
   * @param result The clustering result containing Smile-compatible data.
   * @param leafNames The names of the species, in the order they were initially processed.
   * @param outputPath The path to save the output PNG file.
   * @throws IOException if an I/O error occurs.
   */
  public void saveDendrogram(
      ClusteringResult result, List<String> leafNames, Path outputPath) throws IOException {

    // Create the dendrogram plot using the Smile library
    Dendrogram dendrogram = new Dendrogram(result.smileHc(), leafNames.toArray(new String[0]));

    // Create a canvas to draw the plot on
    Canvas canvas = dendrogram.canvas();
    canvas.setAxisLabels("Species", "Similarity Score (Needleman-Wunsch)");
    canvas.setTitle("Phylogenetic Tree");

    // Ensure the parent directory exists
    Files.createDirectories(outputPath.getParent());

    // Save the canvas to a PNG file
    canvas.toPNG(outputPath.toFile());
  }
}