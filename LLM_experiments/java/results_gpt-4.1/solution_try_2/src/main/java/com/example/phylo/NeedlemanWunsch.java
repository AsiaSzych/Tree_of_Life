package com.example.phylo;

public class NeedlemanWunsch {

    private final BlosumMatrix blosumMatrix;

    public NeedlemanWunsch(BlosumMatrix blosumMatrix) {
        this.blosumMatrix = blosumMatrix;
    }

    public int align(String seq1, String seq2) {
        int m = seq1.length();
        int n = seq2.length();
        int[][] dp = new int[m + 1][n + 1];

        // Initialize first row and column
        dp[0][0] = 0;
        for (int i = 1; i <= m; i++) {
            dp[i][0] = dp[i - 1][0] + blosumMatrix.getDeletionScore(seq1.charAt(i - 1));
        }
        for (int j = 1; j <= n; j++) {
            dp[0][j] = dp[0][j - 1] + blosumMatrix.getDeletionScore(seq2.charAt(j - 1));
        }

        // Fill DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                int match = dp[i - 1][j - 1] + blosumMatrix.getSubstitutionScore(seq1.charAt(i - 1), seq2.charAt(j - 1));
                int delete = dp[i - 1][j] + blosumMatrix.getDeletionScore(seq1.charAt(i - 1));
                int insert = dp[i][j - 1] + blosumMatrix.getDeletionScore(seq2.charAt(j - 1));
                dp[i][j] = Math.max(match, Math.max(delete, insert));
            }
        }
        return dp[m][n];
    }
}