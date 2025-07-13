package com.phylogenetics.service;

import com.phylogenetics.model.TreeNode;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

/**
 * Draws phylogenetic tree as horizontal dendrogram.
 */
public class DendrogramDrawer {
    private static final int IMAGE_WIDTH = 1200;
    private static final int IMAGE_HEIGHT = 800;
    private static final int MARGIN = 50;
    private static final int LEAF_SPACING = 40;
    private static final int LINE_THICKNESS = 2;
    private static final Color LINE_COLOR = Color.BLUE;
    private static final Color TEXT_COLOR = Color.BLACK;
    private static final Font FONT = new Font("Arial", Font.PLAIN, 12);

    public static void drawDendrogram(TreeNode root, String blosumType) throws IOException {
        // Calculate positions and scaling
        Map<TreeNode, Integer> leafPositions = new HashMap<>();
        Map<TreeNode, Integer> nodeDepths = new HashMap<>();
        calculatePositions(root, leafPositions, nodeDepths, 0);

        // Find max score for scaling
        double maxScore = root.getHeight();
        double scale = (IMAGE_WIDTH - 2 * MARGIN) / maxScore;

        // Create image
        BufferedImage image = new BufferedImage(IMAGE_WIDTH, IMAGE_HEIGHT, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = image.createGraphics();
        g.setColor(Color.WHITE);
        g.fillRect(0, 0, IMAGE_WIDTH, IMAGE_HEIGHT);
        g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Draw tree
        drawNode(root, g, leafPositions, nodeDepths, scale, MARGIN);

        // Save to file
        String filename = "./phylogenetic_tree_blosum" + blosumType + ".png";
        ImageIO.write(image, "png", new File(filename));
        g.dispose();
    }

    private static int calculatePositions(TreeNode node, Map<TreeNode, Integer> leafPositions,
                                        Map<TreeNode, Integer> nodeDepths, int position) {
        if (node.isLeaf()) {
            leafPositions.put(node, position);
            nodeDepths.put(node, 0);
            return position + LEAF_SPACING;
        }

        int maxDepth = 0;
        int currentPos = position;
        for (TreeNode child : node.getChildren()) {
            currentPos = calculatePositions(child, leafPositions, nodeDepths, currentPos);
            maxDepth = Math.max(maxDepth, nodeDepths.get(child) + 1);
        }
        nodeDepths.put(node, maxDepth);
        return currentPos;
    }

    private static void drawNode(TreeNode node, Graphics2D g, Map<TreeNode, Integer> leafPositions,
                               Map<TreeNode, Integer> nodeDepths, double scale, int xOffset) {
        if (node.isLeaf()) {
            int y = MARGIN + nodeDepths.get(node) * LEAF_SPACING;
            int x = xOffset + (int)(node.getHeight() * scale);
            g.setColor(TEXT_COLOR);
            g.setFont(FONT);
            g.drawString(node.getName(), x + 5, y + 5);
            return;
        }

        // Calculate positions
        int minPos = Integer.MAX_VALUE;
        int maxPos = Integer.MIN_VALUE;
        int maxChildDepth = 0;
        for (TreeNode child : node.getChildren()) {
            minPos = Math.min(minPos, leafPositions.get(child));
            maxPos = Math.max(maxPos, leafPositions.get(child));
            maxChildDepth = Math.max(maxChildDepth, nodeDepths.get(child));
        }

        int y = MARGIN + maxChildDepth * LEAF_SPACING;
        int x = xOffset + (int)(node.getHeight() * scale);

        // Draw horizontal line
        g.setColor(LINE_COLOR);
        g.setStroke(new BasicStroke(LINE_THICKNESS));
        g.drawLine(x, y, xOffset + (int)(node.getChildren().get(0).getHeight() * scale), y);

        // Draw vertical line and child nodes
        g.drawLine(x, MARGIN + (maxChildDepth - 1) * LEAF_SPACING, x, y);
        for (TreeNode child : node.getChildren()) {
            drawNode(child, g, leafPositions, nodeDepths, scale, xOffset);
        }
    }
}