package com.phylogenetic.visualization;

import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.PhylogeneticTree;
import java.awt.*;
import java.awt.geom.Line2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.imageio.ImageIO;

/**
 * Draws horizontal dendrograms for phylogenetic trees.
 */
public class DendrogramDrawer {
  private static final int MARGIN = 50;
  private static final int LABEL_WIDTH = 150;
  private static final int NODE_HEIGHT = 30;
  private static final int MIN_WIDTH = 800;
  private static final int MIN_HEIGHT = 600;
  
  private final PhylogeneticTree tree;
  private final Map<PhylogeneticNode, Point> nodePositions;
  private int imageWidth;
  private int imageHeight;
  private double scaleFactor;
  
  public DendrogramDrawer(PhylogeneticTree tree) {
    this.tree = tree;
    this.nodePositions = new HashMap<>();
  }
  
  /**
   * Draw the dendrogram and save it to a PNG file.
   */
  public void drawToFile(String filename) throws IOException {
    calculateDimensions();
    BufferedImage image = new BufferedImage(imageWidth, imageHeight, BufferedImage.TYPE_INT_RGB);
    Graphics2D g2d = image.createGraphics();
    
    // Set rendering hints for better quality
    g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
    g2d.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
    
    // White background
    g2d.setColor(Color.WHITE);
    g2d.fillRect(0, 0, imageWidth, imageHeight);
    
    // Draw the tree
    g2d.setColor(Color.BLACK);
    g2d.setStroke(new BasicStroke(2.0f));
    drawNode(g2d, tree.getRoot(), MARGIN, MARGIN, imageHeight - MARGIN);
    
    // Save to file
    g2d.dispose();
    ImageIO.write(image, "PNG", new File(filename));
  }
  
  /**
   * Calculate image dimensions and scaling factor.
   */
  private void calculateDimensions() {
    List<String> species = tree.getAllSpecies();
    int leafCount = species.size();
    
    // Height based on number of species
    imageHeight = Math.max(MIN_HEIGHT, (leafCount * NODE_HEIGHT) + (2 * MARGIN));
    
    // Width based on tree height (max similarity score)
    double treeHeight = tree.getHeight();
    int desiredTreeWidth = MIN_WIDTH - LABEL_WIDTH - (2 * MARGIN);
    scaleFactor = desiredTreeWidth / treeHeight;
    
    imageWidth = MIN_WIDTH;
  }
  
  /**
   * Recursively draw nodes and branches.
   */
  private int drawNode(Graphics2D g2d, PhylogeneticNode node, int x, int yMin, int yMax) {
    if (node.isLeaf()) {
      // Draw leaf node
      int y = (yMin + yMax) / 2;
      
      // Draw the species name
      g2d.setFont(new Font("Arial", Font.PLAIN, 12));
      g2d.drawString(node.getName(), x + 10, y + 5);
      
      // Store position
      nodePositions.put(node, new Point(x, y));
      
      return y;
    } else {
      // Calculate x position based on height (similarity score)
      int nodeX = MARGIN + LABEL_WIDTH + (int)(node.getHeight() * scaleFactor);
      
      // Draw children first
      List<PhylogeneticNode> children = node.getChildren();
      int childrenHeight = yMax - yMin;
      int heightPerChild = childrenHeight / children.size();
      
      int[] childYPositions = new int[children.size()];
      int currentY = yMin;
      
      for (int i = 0; i < children.size(); i++) {
        int childYMin = currentY;
        int childYMax = currentY + heightPerChild;
        childYPositions[i] = drawNode(g2d, children.get(i), x, childYMin, childYMax);
        currentY = childYMax;
      }
      
      // Calculate node Y position (middle of children)
      int nodeY = (childYPositions[0] + childYPositions[childYPositions.length - 1]) / 2;
      
      // Draw horizontal line at this node's height
      g2d.setStroke(new BasicStroke(2.0f));
      g2d.drawLine(nodeX, childYPositions[0], nodeX, childYPositions[childYPositions.length - 1]);
      
      // Draw connections to children
      for (int i = 0; i < children.size(); i++) {
        PhylogeneticNode child = children.get(i);
        Point childPos = nodePositions.get(child);
        if (childPos != null) {
          // Horizontal line from child to this node's vertical line
          g2d.drawLine(childPos.x, childYPositions[i], nodeX, childYPositions[i]);
        }
      }
      
      // Store position
      nodePositions.put(node, new Point(nodeX, nodeY));
      
      return nodeY;
    }
  }
}