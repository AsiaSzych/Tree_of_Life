package com.phylogenetic.io;

import static org.junit.jupiter.api.Assertions.*;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.HashMap;
import java.util.Map;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ResultWriterTest {
  private ResultWriter writer;
  private ObjectMapper objectMapper;
  
  @BeforeEach
  void setUp() {
    writer = new ResultWriter();
    objectMapper = new ObjectMapper();
  }
  
  @AfterEach
  void cleanup() throws IOException {
    // Clean up test files
    Files.deleteIfExists(Path.of("organisms_scores_blosum50.json"));
    Files.deleteIfExists(Path.of("organisms_scores_blosum62.json"));
  }
  
  @Test
  void testSaveScores() throws IOException {
    // Prepare test data
    Map<String, Map<String, Integer>> scoreMatrix = new HashMap<>();
    Map<String, Integer> humanScores = new HashMap<>();
    humanScores.put("Human", 100);
    humanScores.put("Chimp", 95);
    humanScores.put("Mouse", 70);
    scoreMatrix.put("Human", humanScores);
    
    Map<String, Integer> chimpScores = new HashMap<>();
    chimpScores.put("Human", 95);
    chimpScores.put("Chimp", 100);
    chimpScores.put("Mouse", 72);
    scoreMatrix.put("Chimp", chimpScores);
    
    Map<String, Integer> mouseScores = new HashMap<>();
    mouseScores.put("Human", 70);
    mouseScores.put("Chimp", 72);
    mouseScores.put("Mouse", 100);
    scoreMatrix.put("Mouse", mouseScores);
    
    // Save scores
    writer.saveScores(scoreMatrix, "BLOSUM50");
    
    // Verify file exists
    File outputFile = new File("organisms_scores_blosum50.json");
    assertTrue(outputFile.exists());
    
    // Read and verify content
    Map<String, Integer> savedScores = objectMapper.readValue(
        outputFile, new TypeReference<Map<String, Integer>>() {});
    
    // Should have 6 entries (3 unique pairs + 3 self-alignments)
    assertEquals(6, savedScores.size());
    
    // Verify specific scores
    assertEquals(95, savedScores.get("Chimp_Human"));
    assertEquals(70, savedScores.get("Human_Mouse"));
    assertEquals(72, savedScores.get("Chimp_Mouse"));
    assertEquals(100, savedScores.get("Human_Human"));
  }
}