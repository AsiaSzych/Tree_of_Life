package com.phylogenetic.alignment;

import com.phylogenetic.io.DataLoader;
import com.phylogenetic.io.ResultWriter;
import com.phylogenetic.model.AlignmentResult;
import com.phylogenetic.model.BlosumMatrix;
import com.phylogenetic.model.Organism;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Service class that orchestrates the alignment process.
 */
public class AlignmentService {
  private static final Logger logger = LoggerFactory.getLogger(AlignmentService.class);
  private final DataLoader dataLoader;
  private final ResultWriter resultWriter;
  
  public AlignmentService() {
    this.dataLoader = new DataLoader();
    this.resultWriter = new ResultWriter();
  }
  
  /**
   * Runs the complete alignment process with the specified BLOSUM matrix.
   *
   * @param organismsFile path to the organisms JSON file
   * @param blosumFile path to the BLOSUM matrix JSON file
   * @return map of alignment results
   * @throws IOException if files cannot be read or written
   */
  public Map<String, AlignmentResult> runAlignment(String organismsFile, String blosumFile) 
      throws IOException {
    logger.info("Starting alignment process with {} and {}", organismsFile, blosumFile);
    
    // Load data
    List<Organism> organisms = dataLoader.loadOrganisms(organismsFile);
    BlosumMatrix blosumMatrix = dataLoader.loadBlosumMatrix(blosumFile);
    
    // Perform alignments
    SequenceAligner aligner = new SequenceAligner(blosumMatrix);
    Map<String, AlignmentResult> results = aligner.alignAllPairs(organisms);
    
    // Save results
    resultWriter.saveResults(results, blosumMatrix.getMatrixType());
    
    logger.info("Alignment process completed successfully");
    return results;
  }
  
  /**
   * Gets the alignment results and distance matrix for further processing.
   *
   * @param organismsFile path to the organisms JSON file
   * @param blosumFile path to the BLOSUM matrix JSON file
   * @return alignment data containing results and distance matrix
   * @throws IOException if files cannot be read
   */
  public AlignmentData getAlignmentData(String organismsFile, String blosumFile) 
      throws IOException {
    List<Organism> organisms = dataLoader.loadOrganisms(organismsFile);
    Map<String, AlignmentResult> results = runAlignment(organismsFile, blosumFile);
    
    SequenceAligner aligner = new SequenceAligner(
        dataLoader.loadBlosumMatrix(blosumFile));
    int[][] distanceMatrix = aligner.createDistanceMatrix(organisms, results);
    
    return new AlignmentData(organisms, results, distanceMatrix);
  }
  
  /**
   * Container for alignment data needed by downstream processes.
   */
  public record AlignmentData(
      List<Organism> organisms,
      Map<String, AlignmentResult> alignmentResults,
      int[][] distanceMatrix) {}
}