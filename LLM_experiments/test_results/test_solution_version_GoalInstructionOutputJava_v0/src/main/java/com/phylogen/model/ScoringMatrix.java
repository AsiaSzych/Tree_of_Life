package com.phylogen.model;

import java.util.Map;
import java.util.NoSuchElementException;

/**
 * A wrapper for the BLOSUM scoring data.
 * It provides a clean interface to get substitution scores and gap penalties.
 */
public class ScoringMatrix {

    private final Map<String, Integer> scores;

    public ScoringMatrix(Map<String, Integer> scores) {
        this.scores = scores;
    }

    /**
     * Gets the score for substituting character c1 with c2.
     * The lookup is symmetrical (e.g., "AG" is the same as "GA").
     *
     * @param c1 First character.
     * @param c2 Second character.
     * @return The substitution score.
     * @throws NoSuchElementException if the score for the pair is not in the matrix.
     */
    public int getSubstitutionScore(char c1, char c2) {
        String key1 = "" + c1 + c2;
        String key2 = "" + c2 + c1;

        if (scores.containsKey(key1)) {
            return scores.get(key1);
        } else if (scores.containsKey(key2)) {
            return scores.get(key2);
        }
        throw new NoSuchElementException("Score for substitution " + c1 + "/" + c2 + " not found in scoring matrix.");
    }

    /**
     * Gets the penalty for a gap corresponding to the given character.
     *
     * @param c The character being aligned with a gap.
     * @return The gap penalty score.
     * @throws NoSuchElementException if the gap penalty for the character is not in the matrix.
     */
    public int getGapPenalty(char c) {
        String key = String.valueOf(c);
        if (scores.containsKey(key)) {
            return scores.get(key);
        }
        throw new NoSuchElementException("Gap penalty for character '" + c + "' not found in scoring matrix.");
    }
}