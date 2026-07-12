package com.example.phylo;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.util.List;
import javax.imageio.ImageIO;

public class DendrogramDrawer {

  private static final int MARGIN_LEFT = 100;
  private static final int MARGIN_TOP = 40;
  private static final int MARGIN_BOTTOM = 40;
  private static final int NODE_RADIUS = 4;
  private static final int FONT_SIZE = 14;
  private static final int VERTICAL_SPACING = 40;

  /**
   * Draws a horizontal dendrogram and saves it as a PNG file.
   * @param root The root of the tree.
   * @param filename The output PNG file.
   */
  public static void drawDendrogram(PhyloNode root, String filename) throws Exception {
    int leafCount = root.getLeafNames().size();
    int imgHeight = MARGIN_TOP + MARGIN_BOTTOM + leafCount * VERTICAL_SPACING;
    int imgWidth = 1000; // Will be adjusted based on max score

    int maxScore = getMaxHeight(root);

    // If all scores are negative (shouldn't happen), set to 1 to avoid division by zero
    if (maxScore <= 0) {
      maxScore = 1;
    }

    BufferedImage image = new BufferedImage(imgWidth, imgHeight, BufferedImage.TYPE_INT_ARGB);
    Graphics2D g = image.createGraphics();

    // Anti-aliasing for better quality
    g.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);

    // White background
    g.setColor(Color.WHITE);
    g.fillRect(0, 0, imgWidth, imgHeight);

    // Draw the tree
    int[] yPos = {MARGIN_TOP};
    drawNode(g, root, MARGIN_LEFT, imgWidth - 40, yPos, maxScore);

    // Draw axis
    g.setColor(Color.BLACK);
    g.setStroke(new BasicStroke(1.2f));
    g.drawLine(MARGIN_LEFT, imgHeight - MARGIN_BOTTOM, imgWidth - 40, imgHeight - MARGIN_BOTTOM);
    g.setFont(new Font("Arial", Font.PLAIN, 12));
    g.drawString("Similarity (Needleman-Wunsch score)", imgWidth / 2 - 80, imgHeight - 10);

    g.dispose();
    ImageIO.write(image, "png", new File(filename));
  }

  /**
   * Recursively draws the tree.
   * @return The y-coordinate of the node.
   */
  private static int drawNode(Graphics2D g, PhyloNode node, int minX, int maxX, int[] yPos, int maxScore) {
    if (node.isLeaf()) {
      int y = yPos[0];
      int x = scoreToX(node.getHeight(), minX, maxX, maxScore);
      g.setColor(Color.BLUE);
      g.fillOval(x - NODE_RADIUS, y - NODE_RADIUS, NODE_RADIUS * 2, NODE_RADIUS * 2);
      g.setColor(Color.BLACK);
      g.setFont(new Font("Arial", Font.PLAIN, FONT_SIZE));
      g.drawString(node.getName(), x + 8, y + 5);
      yPos[0] += VERTICAL_SPACING;
      return y;
    } else {
      List<PhyloNode> children = node.getChildren();
      int[] childYs = new int[children.size()];
      int thisX = scoreToX(node.getHeight(), minX, maxX, maxScore);

      // Draw children and collect their y positions
      for (int i = 0; i < children.size(); i++) {
        childYs[i] = drawNode(g, children.get(i), minX, maxX, yPos, maxScore);
      }

      int minY = childYs[0];
      int maxY = childYs[childYs.length - 1];

      // Draw vertical line connecting children
      g.setColor(Color.BLACK);
      g.setStroke(new BasicStroke(2.0f));
      g.drawLine(thisX, minY, thisX, maxY);

      // Draw horizontal lines to children
      for (int childY : childYs) {
        int childX = scoreToX(children.get(0).isLeaf() ? node.getHeight() : children.get(0).getHeight(), minX, maxX, maxScore);
        int childNodeX = scoreToX(getChildHeightForLine(node, childY, children, childYs), minX, maxX, maxScore);
        g.drawLine(thisX, childY, childNodeX, childY);
      }

      return (minY + maxY) / 2;
    }
  }

  /**
   * Converts a similarity score to an x-coordinate.
   */
  private static int scoreToX(int score, int minX, int maxX, int maxScore) {
    // Map [0, maxScore] to [minX, maxX]
    if (score < 0) score = 0;
    return minX + (int) ((score / (double) maxScore) * (maxX - minX));
  }

  /**
   * Returns the maximum height (score) in the tree.
   */
  private static int getMaxHeight(PhyloNode node) {
    int h = node.getHeight();
    for (PhyloNode child : node.getChildren()) {
      h = Math.max(h, getMaxHeight(child));
    }
    return h;
  }

  /**
   * Helper to get the height for a child node given its y position.
   */
  private static int getChildHeightForLine(PhyloNode parent, int childY, List<PhyloNode> children, int[] childYs) {
    for (int i = 0; i < children.size(); i++) {
      if (childYs[i] == childY) {
        return children.get(i).getHeight() < 0 ? 0 : children.get(i).getHeight();
      }
    }
    return 0;
  }
}