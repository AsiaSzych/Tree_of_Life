package com.phylogenetic.visualization;

import com.phylogenetic.tree.PhylogeneticNode;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.imageio.ImageIO;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Creates dendrogram visualizations of phylogenetic trees.
 */
public class DendrogramDrawer {
  private static final Logger logger = LoggerFactory.getLogger(DendrogramDrawer.class);
  
  private static final int MARGIN = 50;
  private static final int LABEL_WIDTH = 150;
  private static final int NODE_SIZE = 6;
  private static final int FONT_SIZE = 12;
  private static final int VERTICAL_SPACING = 30;
  
  private final Map<String, Integer> leafYPositions = new HashMap<>();
  private int currentY = MARGIN;
  
  /**
   * Draws and saves a dendrogram of the phylogenetic tree.
   *
   * @param root root of the phylogenetic tree
   * @param blosumType the BLOSUM matrix type used
   * @throws IOException if file cannot be saved
   */
  public void drawDendrogram(PhylogeneticNode root, String blosumType) throws IOException {
    String blosumNumber = blosumType.replaceAll("[^0-9]", "");
    String filename = String.format("phylogenetic_tree_blosum%s.png", blosumNumber);
    
    logger.info("Creating dendrogram visualization: {}", filename);
    
    // Calculate dimensions
    List<String> leaves = root.getLeafNames();
    int height = (leaves.size() * VERTICAL_SPACING) + (2 * MARGIN);
    int width = calculateWidth(root) + LABEL_WIDTH + (2 * MARGIN);
    
    // Create image
    BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
    Graphics2D g2d = image.createGraphics();
    
    // Set rendering hints for better quality
    g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, 
        RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
    
    // White background
    g2d.setColor(Color.WHITE);
    g2d.fillRect(0, 0, width, height);
    
    // Calculate leaf positions
    calculateLeafPositions(root);
    
    // Draw the tree
    g2d.setColor(Color.BLACK);
    g2d.setStroke(new BasicStroke(2));
    drawNode(g2d, root, MARGIN, width - MARGIN - LABEL_WIDTH);
    
    // Draw scale
    drawScale(g2d, width, height, root.getHeight());
    
    g2d.dispose();
    
    // Save image
    File outputFile = new File(filename);
    ImageIO.write(image, "PNG", outputFile);
    
    logger.info("Dendrogram saved to: {}", filename);
  }
  
  /**
   * Calculates Y positions for all leaf nodes.
   *
   * @param node current node
   */
  private void calculateLeafPositions(PhylogeneticNode node) {
    if (node.isLeaf()) {
      leafYPositions.put(node.getName(), currentY);
      currentY += VERTICAL_SPACING;
    } else {
      if (node.getLeft() != null) {
        calculateLeafPositions(node.getLeft());
      }
      if (node.getRight() != null) {
        calculateLeafPositions(node.getRight());
      }
    }
  }
  
  /**
   * Draws a node and its subtree.
   *
   * @param g2d graphics context
   * @param node node to draw
   * @param minX minimum X coordinate
   * @param maxX maximum X coordinate
   * @return Y coordinate of this node
   */
  private int drawNode(Graphics2D g2d, PhylogeneticNode node, int minX, int maxX) {
    if (node.isLeaf()) {
      // Draw leaf label
      int y = leafYPositions.get(node.getName());
      g2d.setFont(new Font("Arial", Font.PLAIN, FONT_SIZE));
      g2d.drawString(node.getName(), maxX + 10, y + 5);
      
      // Draw leaf node
      g2d.fillOval(maxX - NODE_SIZE/2, y - NODE_SIZE/2, NODE_SIZE, NODE_SIZE);
      return y;
    } else {
      // Calculate X position based on height (similarity score)
      double heightRatio = node.getHeight() / getMaxHeight(node);
      int x = maxX - (int)((maxX - minX) * (1 - heightRatio));
      
      // Draw children
      int leftY = 0, rightY = 0;
      if (node.getLeft() != null) {
        leftY = drawNode(g2d, node.getLeft(), minX, x);
        // Draw horizontal line to left child
        int leftX = calculateNodeX(node.getLeft(), minX, x);
        g2d.drawLine(x, leftY, leftX, leftY);
      }
      
      if (node.getRight() != null) {
        rightY = drawNode(g2d, node.getRight(), minX, x);
        // Draw horizontal line to right child
        int rightX = calculateNodeX(node.getRight(), minX, x);
        g2d.drawLine(x, rightY, rightX, rightY);
      }
      
      // Draw vertical line connecting children
      int nodeY = (leftY + rightY) / 2;
      g2d.drawLine(x, leftY, x, rightY);
      
      // Draw node
      g2d.fillOval(x - NODE_SIZE/2, nodeY - NODE_SIZE/2, NODE_SIZE, NODE_SIZE);
      
      return nodeY;
    }
  }
  
  /**
   * Calculates X position for a node based on its height.
   *
   * @param node node to position
   * @param minX minimum X coordinate
   * @param maxX maximum X coordinate
   * @return X coordinate
   */
  private int calculateNodeX(PhylogeneticNode node, int minX, int maxX) {
    if (node.isLeaf()) {
      return maxX;
    }
    double heightRatio = node.getHeight() / getMaxHeight(node);
    return maxX - (int)((maxX - minX) * (1 - heightRatio));
  }
  
  /**
   * Gets the maximum height in the tree.
   *
   * @param node root node
   * @return maximum height
   */
  private double getMaxHeight(PhylogeneticNode node) {
    double maxHeight = node.getHeight();
    PhylogeneticNode current = node;
    while (!current.isLeaf()) {
      if (current.getLeft() != null && !current.getLeft().isLeaf()) {
        current = current.getLeft();
      } else if (current.getRight() != null && !current.getRight().isLeaf()) {
        current = current.getRight();
      } else {
        break;
      }
      maxHeight = Math.max(maxHeight, current.getHeight());
    }
    return maxHeight;
  }
  
  /**
   * Calculates required width based on tree height.
   *
   * @param root root node
   * @return required width
   */
  private int calculateWidth(PhylogeneticNode root) {
    // Width proportional to tree height
    return Math.max(600, (int)(root.getHeight() * 0.5));
  }
  
  /**
   * Draws a scale bar on the dendrogram.
   *
   * @param g2d graphics context
   * @param width image width
   * @param height image height
   * @param maxScore maximum similarity score
   */
  private void drawScale(Graphics2D g2d, int width, int height, double maxScore) {
    int scaleY = height - 30;
    int scaleStartX = MARGIN;
    int scaleEndX = width - MARGIN - LABEL_WIDTH;
    int scaleLength = scaleEndX - scaleStartX;
    
    // Draw scale line
    g2d.setStroke(new BasicStroke(1));
    g2d.drawLine(scaleStartX, scaleY, scaleEndX, scaleY);
    
    // Draw scale ticks and labels
    g2d.setFont(new Font("Arial", Font.PLAIN, 10));
    int numTicks = 5;
    for (int i = 0; i <= numTicks; i++) {
      int x = scaleStartX + (scaleLength * i / numTicks);
      g2d.drawLine(x, scaleY - 3, x, scaleY + 3);
      
      int score = (int)(maxScore * (1 - (double)i / numTicks));
      String label = String.valueOf(score);
      FontMetrics fm = g2d.getFontMetrics();
      int labelWidth = fm.stringWidth(label);
      g2d.drawString(label, x - labelWidth/2, scaleY + 15);
    }
    
    // Scale label
    g2d.drawString("Similarity Score", scaleStartX + scaleLength/2 - 40, scaleY + 25);
  }
}