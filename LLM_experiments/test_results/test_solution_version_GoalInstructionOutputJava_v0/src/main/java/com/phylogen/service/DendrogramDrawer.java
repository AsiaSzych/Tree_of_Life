package com.phylogen.service;

import com.phylogen.model.TreeNode;

import javax.imageio.ImageIO;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Service to draw a dendrogram from a TreeNode structure and save it as a PNG file.
 */
public class DendrogramDrawer {

    // --- Configuration Constants for Drawing ---
    private static final int PADDING = 50;
    private static final int LEAF_VERTICAL_SPACING = 30;
    private static final int LEAF_NAME_OFFSET = 10;
    private static final Font LEAF_FONT = new Font("Arial", Font.PLAIN, 12);
    private static final Color LINE_COLOR = Color.DARK_GRAY;
    private static final Color TEXT_COLOR = Color.BLACK;
    private static final float LINE_THICKNESS = 1.5f;

    private Graphics2D g2d;
    private int imageWidth;
    private int minScore;
    private int maxScore;
    private AtomicInteger currentY;

    /**
     * Draws the dendrogram and saves it to a file.
     *
     * @param root       The root node of the tree.
     * @param outputPath The path to save the output PNG file.
     * @throws IOException if there is an error writing the file.
     */
    public void drawAndSave(TreeNode root, Path outputPath) throws IOException {
        // 1. Pre-calculation step to determine image dimensions and score range
        List<TreeNode> leaves = root.getLeafDescendants();
        int imageHeight = (leaves.size() * LEAF_VERTICAL_SPACING) + (2 * PADDING);
        this.imageWidth = 1200; // A fixed width, can be made dynamic if needed
        this.currentY = new AtomicInteger(PADDING);

        findScoreRange(root);

        // 2. Setup image and graphics context
        BufferedImage image = new BufferedImage(imageWidth, imageHeight, BufferedImage.TYPE_INT_ARGB);
        this.g2d = image.createGraphics();
        setupGraphics();

        // 3. Recursively draw the tree
        drawNodeRecursive(root);

        // 4. Save the image to a file
        g2d.dispose();
        ImageIO.write(image, "PNG", outputPath.toFile());
    }

    private void setupGraphics() {
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2d.setColor(Color.WHITE);
        g2d.fillRect(0, 0, imageWidth, imageWidth);
        g2d.setColor(LINE_COLOR);
        g2d.setStroke(new BasicStroke(LINE_THICKNESS));
        g2d.setFont(LEAF_FONT);
    }

    /**
     * Recursively draws a node and its descendants.
     *
     * @param node The current node to draw.
     * @return The Y-coordinate of the horizontal line for this node.
     */
    private int drawNodeRecursive(TreeNode node) {
        // The X-coordinate is determined by the similarity score
        int x = getXForScore(node.getSimilarityScore().orElse(maxScore));

        // Base case: a leaf node
        if (node.isLeaf()) {
            int y = currentY.getAndAdd(LEAF_VERTICAL_SPACING);
            g2d.setColor(TEXT_COLOR);
            g2d.drawString(node.getSpeciesName().orElse("?"), x + LEAF_NAME_OFFSET, y + (LEAF_FONT.getSize() / 2) - 2);
            return y;
        }

        // Recursive step: an internal node
        // Draw children first to get their Y-coordinates
        int firstChildY = -1;
        int lastChildY = -1;
        for (TreeNode child : node.getChildren()) {
            int childY = drawNodeRecursive(child);
            if (firstChildY == -1) {
                firstChildY = childY;
            }
            lastChildY = childY;

            // Draw horizontal line from child to this node's vertical line
            int childX = getXForScore(child.getSimilarityScore().orElse(maxScore));
            g2d.setColor(LINE_COLOR);
            g2d.drawLine(x, childY, childX, childY);
        }

        // Draw the vertical connector line for this node
        int nodeY = (firstChildY + lastChildY) / 2;
        g2d.drawLine(x, firstChildY, x, lastChildY);

        return nodeY;
    }

    /**
     * Maps a similarity score to a horizontal pixel coordinate.
     */
    private int getXForScore(int score) {
        double scoreRange = maxScore - minScore;
        if (scoreRange <= 0) return PADDING; // Avoid division by zero
        double availableWidth = imageWidth - (2.0 * PADDING);
        double relativeScore = score - minScore;
        return (int) (PADDING + (relativeScore / scoreRange) * availableWidth);
    }

    /**
     * Traverses the tree to find the minimum and maximum similarity scores for scaling.
     */
    private void findScoreRange(TreeNode node) {
        minScore = Integer.MAX_VALUE;
        maxScore = Integer.MIN_VALUE;
        findScoreRangeRecursive(node);
    }

    private void findScoreRangeRecursive(TreeNode node) {
        if (node.isLeaf()) return;

        int score = node.getSimilarityScore().orElseThrow();
        if (score < minScore) minScore = score;
        if (score > maxScore) maxScore = score;

        for (TreeNode child : node.getChildren()) {
            findScoreRangeRecursive(child);
        }
    }
}