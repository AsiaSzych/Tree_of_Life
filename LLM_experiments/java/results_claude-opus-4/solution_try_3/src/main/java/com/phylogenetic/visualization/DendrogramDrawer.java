package com.phylogenetic.visualization;

import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.PhylogeneticTree;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.geom.Line2D;
import java.awt.geom.Rectangle2D;
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
 * Draws horizontal dendrograms of phylogenetic trees.
 */
public class DendrogramDrawer {
  private static final Logger logger = LoggerFactory.getLogger(DendrogramDrawer.class);
  
  private static final int MARGIN = 50;
  private static final int LABEL_MARGIN = 10;
  private static final int MIN_LEAF_SPACING = 30;
  private static final int DEFAULT_WIDTH = 1200;
  private static final int MIN_HEIGHT = 400;
  private static final Color BRANCH_COLOR = new Color(50, 50, 50);
  private static final Color LABEL_COLOR = new Color(30, 30, 30);
  private static final Font LABEL_FONT = new Font("Arial", Font.PLAIN, 12);
  private static final Font SCALE_FONT = new Font("Arial", Font.PLAIN, 10);
  
  /**
   * Draw and save a dendrogram of the phylogenetic tree.
   */
  public void drawDendrogram(PhylogeneticTree tree, String filename) throws IOException {
    logger.info("Drawing dendrogram to file: {}", filename);
    
    // Calculate tree layout
    TreeLayout layout = calculateLayout(tree);
    
    // Create image
    int width = DEFAULT_WIDTH;
    int height = Math.max(MIN_HEIGHT, layout.leafCount * MIN_LEAF_SPACING + 2 * MARGIN);
    BufferedImage image = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
    
    // Draw on image
    Graphics2D g2d = image.createGraphics();
    setupGraphics(g2d);
    
    // Fill background
    g2d.setColor(Color.WHITE);
    g2d.fillRect(0, 0, width, height);
    
    // Draw the tree
    drawTree(g2d, tree, layout, width, height);
    
    // Draw scale
    drawScale(g2d, tree, layout, width, height);
    
    g2d.dispose();
    
    // Save to file
    File outputFile = new File(filename);
    ImageIO.write(image, "PNG", outputFile);
    
    logger.info("Dendrogram saved successfully");
  }
  
  /**
   * Set up graphics rendering hints for better quality.
   */
  private void setupGraphics(Graphics2D g2d) {
    g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, 
        RenderingHints.VALUE_ANTIALIAS_ON);
    g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, 
        RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
  }
  
  /**
   * Calculate the layout positions for all nodes in the tree.
   */
  private TreeLayout calculateLayout(PhylogeneticTree tree) {
    TreeLayout layout = new TreeLayout();
    List<String> leafOrder = tree.getAllSpecies();
    layout.leafCount = leafOrder.size();
    
    // Assign Y positions to leaves
    double leafSpacing = 1.0 / (leafOrder.size() + 1);
    for (int i = 0; i < leafOrder.size(); i++) {
      layout.leafYPositions.put(leafOrder.get(i), (i + 1) * leafSpacing);
    }
    
    // Calculate positions for all nodes
    calculateNodePositions(tree.getRoot(), layout);
    
    return layout;
  }
  
  /**
   * Recursively calculate Y positions for internal nodes.
   */
  private double calculateNodePositions(PhylogeneticNode node, TreeLayout layout) {
    if (node.isLeaf()) {
      return layout.leafYPositions.get(node.getName());
    }
    
    // Calculate Y position as average of children
    double leftY = calculateNodePositions(node.getLeft(), layout);
    double rightY = calculateNodePositions(node.getRight(), layout);
    double nodeY = (leftY + rightY) / 2.0;
    
    layout.nodeYPositions.put(node, nodeY);
    return nodeY;
  }
  
  /**
   * Draw the tree structure.
   */
  private void drawTree(Graphics2D g2d, PhylogeneticTree tree, TreeLayout layout, 
      int width, int height) {
    // Calculate scaling for X coordinates
    int drawWidth = width - 2 * MARGIN - 150; // Leave space for labels
    double xScale = drawWidth / (double) tree.getMaxScore();
    
    // Draw branches
    g2d.setColor(BRANCH_COLOR);
    g2d.setStroke(new BasicStroke(2.0f));
    drawNode(g2d, tree.getRoot(), layout, xScale, height, tree.getMaxScore());
    
    // Draw leaf labels
    g2d.setColor(LABEL_COLOR);
    g2d.setFont(LABEL_FONT);
    for (Map.Entry<String, Double> entry : layout.leafYPositions.entrySet()) {
      String leafName = entry.getKey();
      double yPos = entry.getValue() * (height - 2 * MARGIN) + MARGIN;
      
      // Draw label at the right edge
      g2d.drawString(leafName, width - MARGIN - 140, (float) yPos + 4);
    }
  }
  
  /**
   * Recursively draw nodes and branches.
   */
  private void drawNode(Graphics2D g2d, PhylogeneticNode node, TreeLayout layout, 
      double xScale, int height, int maxScore) {
    if (node.isLeaf()) {
      return;
    }
    
    // Get positions
    double nodeY = layout.nodeYPositions.get(node) * (height - 2 * MARGIN) + MARGIN;
    double nodeX = MARGIN + (maxScore - node.getHeight()) * xScale;
    
    // Draw branches to children
    if (node.getLeft() != null) {
      drawBranchToChild(g2d, node.getLeft(), nodeX, nodeY, layout, xScale, 
          height, maxScore);
    }
    if (node.getRight() != null) {
      drawBranchToChild(g2d, node.getRight(), nodeX, nodeY, layout, xScale, 
          height, maxScore);
    }
    
    // Recursively draw children
    drawNode(g2d, node.getLeft(), layout, xScale, height, maxScore);
    drawNode(g2d, node.getRight(), layout, xScale, height, maxScore);
  }
  
  /**
   * Draw branch from parent to child.
   */
  private void drawBranchToChild(Graphics2D g2d, PhylogeneticNode child, 
      double parentX, double parentY, TreeLayout layout, double xScale, 
      int height, int maxScore) {
    
    double childY;
    if (child.isLeaf()) {
      childY = layout.leafYPositions.get(child.getName()) * (height - 2 * MARGIN) 
          + MARGIN;
    } else {
      childY = layout.nodeYPositions.get(child) * (height - 2 * MARGIN) + MARGIN;
    }
    
    double childX = MARGIN + (maxScore - child.getHeight()) * xScale;
    
    // Draw horizontal line from parent
    g2d.draw(new Line2D.Double(parentX, parentY, childX, parentY));
    
    // Draw vertical line to child
    g2d.draw(new Line2D.Double(childX, parentY, childX, childY));
    
    // Draw horizontal line to child (if it's a leaf)
    if (child.isLeaf()) {
      double leafEndX = MARGIN + maxScore * xScale;
      g2d.draw(new Line2D.Double(childX, childY, leafEndX, childY));
    }
  }
  
  /**
   * Draw scale bar and axis.
   */
  private void drawScale(Graphics2D g2d, PhylogeneticTree tree, TreeLayout layout, 
      int width, int height) {
    g2d.setColor(LABEL_COLOR);
    g2d.setFont(SCALE_FONT);
    
    // Draw X axis
    int axisY = height - MARGIN + 20;
    int axisStartX = MARGIN;
    int axisEndX = width - MARGIN - 150;
    
    g2d.draw(new Line2D.Double(axisStartX, axisY, axisEndX, axisY));
    
    // Draw scale ticks and labels
    int numTicks = 5;
    double scoreRange = tree.getMaxScore() - tree.getMinScore();
    
    for (int i = 0; i <= numTicks; i++) {
      double fraction = i / (double) numTicks;
      int tickX = (int) (axisStartX + fraction * (axisEndX - axisStartX));
      int score = (int) (tree.getMaxScore() - fraction * scoreRange);
      
      // Draw tick
      g2d.draw(new Line2D.Double(tickX, axisY - 3, tickX, axisY + 3));
      
      // Draw label
      String label = String.valueOf(score);
      Rectangle2D bounds = g2d.getFontMetrics().getStringBounds(label, g2d);
      g2d.drawString(label, (float) (tickX - bounds.getWidth() / 2), axisY + 15);
    }
    
    // Draw axis label
    g2d.drawString("Needleman-Wunsch Similarity Score", 
        axisStartX + (axisEndX - axisStartX) / 2 - 80, axisY + 30);
  }
  
  /**
   * Helper class to store tree layout information.
   */
  private static class TreeLayout {
    Map<String, Double> leafYPositions = new HashMap<>();
    Map<PhylogeneticNode, Double> nodeYPositions = new HashMap<>();
    int leafCount = 0;
  }
}