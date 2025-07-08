package com.phylogenetic.alignment;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.phylogenetic.model.BlosumMatrix;
import java.util.Map;
import org.junit.jupiter.api.Test;

/**
 * Tests for the Needleman-Wunsch implementation.
 */
class NeedlemanWunschTest {
  
  @Test
  void testExampleCase() {
    // Test case from the requirements
    Map<String, Integer> scores = Map.of(
        "a", -1,
        "b", -2,
        "ab", -3,
        "ba", -3,
        "aa", 2,
        "bb", 3
    );
    
    BlosumMatrix matrix = new BlosumMatrix(scores, "TEST");
    NeedlemanWunsch aligner = new NeedlemanWunsch(matrix);
    
    int score = aligner.calculateScore("aabaab", "ababaa");
    assertEquals(7, score, "Score should match the expected value of 7");
  }
}