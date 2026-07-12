package com.phylogenetic;

import com.phylogenetic.alignment.AlignmentService;
import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.tree.PhylogeneticNode;
import java.io.IOException;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main entry point for the sequence alignment application.
 */
public class Main {
  private static final Logger logger = LoggerFactory.getLogger(Main.class);
  
  public static void main(String[] args) {
    try {
      AlignmentService alignmentService = new AlignmentService();
      
      // Determine which BLOSUM matrix to use
      String blosumFile = "blosum62.json"; // Default
      String organismFile = "organisms.json"; // Default
      String thresholdFile = "thresholds.txt"; // Default
      if (args.length > 0) {
        blosumFile = args[0];
      }
      
      logger.info("Running alignment with BLOSUM matrix: {}", blosumFile);
      
      // Run the alignment process
      Map<String, AlignmentResult> results = alignmentService.runAlignment(
          "organisms.json", 
          blosumFile
      );
      
      // Log some statistics
      logger.info("Alignment complete. Processed {} organism pairs", results.size());
      
      // Example: print a few results
      results.entrySet().stream()
          .limit(5)
          .forEach(entry -> {
            AlignmentResult result = entry.getValue();
            logger.info("Alignment score for {} vs {}: {}", 
                result.organism1(), 
                result.organism2(), 
                result.score());
          });
      
    
      PhylogeneticAnalysis analysis = new PhylogeneticAnalysis();
      PhylogeneticNode root = analysis.runAnalysis(organismFile, blosumFile, thresholdFile);

    } catch (IOException e) {
      logger.error("Error during alignment process", e);
      System.exit(1);
    }

  }
}