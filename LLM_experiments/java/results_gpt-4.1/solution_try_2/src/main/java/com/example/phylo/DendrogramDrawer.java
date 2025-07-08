package com.example.phylo;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.List;
import javax.imageio.ImageIO;

public class DendrogramDrawer {

    private static final int LEAF_HEIGHT = 40;
    private static final int NODE_RADIUS = 4;
    private static final int PADDING_LEFT = 100;
    private static final int PADDING_TOP = 40;
    private static final int PADDING_RIGHT = 40;
    private static final int PADDING_BOTTOM = 40;
    private static final int FONT_SIZE = 16;

    public static void drawDendrogram(PhyloNode root, String filePath) throws IOException {
        int leafCount = root.getLeafNames().size();
        int imgHeight = PADDING_TOP + PADDING_BOTTOM + LEAF_HEIGHT * leafCount;
        int imgWidth = 1200; // can be adjusted

        int maxHeight = root.getHeight();

        BufferedImage image = new BufferedImage(imgWidth, imgHeight, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = image.createGraphics();

        // White background
        g2.setColor(Color.WHITE);
        g2.fillRect(0, 0, imgWidth, imgHeight);

        // Anti-aliasing
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

        // Draw dendrogram
        int[] yPos = {PADDING_TOP};
        drawNode(g2, root, maxHeight, PADDING_LEFT, imgWidth - PADDING_RIGHT, yPos, imgHeight);

        // Draw axis
        g2.setColor(Color.BLACK);
        g2.setStroke(new BasicStroke(1.5f));
        g2.drawLine(PADDING_LEFT, imgHeight - PADDING_BOTTOM, imgWidth - PADDING_RIGHT, imgHeight - PADDING_BOTTOM);
        g2.setFont(new Font("Arial", Font.PLAIN, 12));
        g2.drawString("Needleman-Wunsch Similarity", imgWidth / 2 - 80, imgHeight - 10);

        g2.dispose();
        ImageIO.write(image, "png", new File(filePath));
    }

    private static int drawNode(Graphics2D g2, PhyloNode node, int maxHeight, int xStart, int xEnd, int[] yPos, int imgHeight) {
        if (node.isLeaf()) {
            int y = yPos[0];
            int x = xEnd;
            g2.setColor(Color.BLACK);
            g2.setFont(new Font("Arial", Font.PLAIN, FONT_SIZE));
            g2.drawString(node.getName(), x + 10, y + FONT_SIZE / 2);
            // Draw a small circle at the leaf
            g2.fillOval(x - NODE_RADIUS, y - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2);
            yPos[0] += LEAF_HEIGHT;
            return y;
        } else {
            // Calculate x position based on similarity score (height)
            int nodeX = xStart + (int) ((xEnd - xStart) * (node.getHeight() / (double) maxHeight));
            int leftY = drawNode(g2, node.getLeft(), maxHeight, xStart, xEnd, yPos, imgHeight);
            int rightY = drawNode(g2, node.getRight(), maxHeight, xStart, xEnd, yPos, imgHeight);
            int y = (leftY + rightY) / 2;

            // Draw horizontal line between children
            int leftChildX = xStart + (int) ((xEnd - xStart) * (node.getLeft().isLeaf() ? 0 : node.getLeft().getHeight() / (double) maxHeight));
            int rightChildX = xStart + (int) ((xEnd - xStart) * (node.getRight().isLeaf() ? 0 : node.getRight().getHeight() / (double) maxHeight));

            g2.setColor(Color.BLUE);
            g2.setStroke(new BasicStroke(2.0f));
            // Vertical line
            g2.drawLine(nodeX, leftY, nodeX, rightY);
            // Horizontal lines to children
            g2.drawLine(leftChildX, leftY, nodeX, leftY);
            g2.drawLine(rightChildX, rightY, nodeX, rightY);

            // Draw node circle
            g2.setColor(Color.RED);
            g2.fillOval(nodeX - NODE_RADIUS, y - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2);

            // Draw similarity score at node
            g2.setColor(Color.BLACK);
            g2.setFont(new Font("Arial", Font.PLAIN, 12));
            g2.drawString(String.valueOf(node.getHeight()), nodeX - 10, y - 8);

            return y;
        }
    }
}