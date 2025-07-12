package com.phylogenetic.visualization;

import com.phylogenetic.tree.PhylogeneticNode;
import com.phylogenetic.tree.PhylogeneticTree;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Enhanced dendrogram drawer using JFreeChart for better visualization.
 */
public class EnhancedDendrogramDrawer {
  private final PhylogeneticTree tree;
  private final Map<PhylogeneticNode, Double> nodeYPositions;
  private final XYSeriesCollection dataset;
  private int nextLeafPosition;
  
  public EnhancedDendrogramDrawer(PhylogeneticTree tree) {
    this.tree = tree;
    this.nodeYPositions = new HashMap<>();
    this.dataset = new XYSeriesCollection();
    this.nextLeafPosition = 0;
  }
  
  /**
   * Create and save the dendrogram chart.
   */
  public void drawToFile(String filename) throws IOException {
    // Calculate positions
    calculateNodePositions(tree.getRoot());
    
    // Create the chart
    JFreeChart chart = ChartFactory.createXYLineChart(
        "Phylogenetic Tree Dendrogram",
        "Needleman-Wunsch Similarity Score",
        "Species",
        dataset,
        PlotOrientation.HORIZONTAL,
        false,
        true,
        false
    );
    
    // Customize the plot
    XYPlot plot = chart.getXYPlot();
    plot.setBackgroundPaint(Color.WHITE);
    plot.setDomainGridlinePaint(Color.LIGHT_GRAY);
    plot.setRangeGridlinePaint(Color.LIGHT_GRAY);
    
    // Set up renderer
    XYLineAndShapeRenderer renderer = new XYLineAndShapeRenderer();
    renderer.setDefaultShapesVisible(false);
    renderer.setDefaultLinesVisible(true);
    renderer.setDefaultStroke(new BasicStroke(2.0f));
    renderer.setDefaultPaint(Color.BLACK);
    plot.setRenderer(renderer);
    
    // Customize axes
    NumberAxis domainAxis = (NumberAxis) plot.getDomainAxis();
    domainAxis.setAutoRangeIncludesZero(true);
    
    NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
    rangeAxis.setVisible(false);
    
    // Add series for drawing the dendrogram
    drawDendrogramLines(tree.getRoot());
    
    // Save the chart
    int width = 1200;
    int height = Math.max(800, tree.getAllSpecies().size() * 40);
    ChartUtils.saveChartAsPNG(new File(filename), chart, width, height);
  }
  
  /**
   * Calculate Y positions for all nodes.
   */
  private double calculateNodePositions(PhylogeneticNode node) {
    if (node.isLeaf()) {
      double yPos = nextLeafPosition++;
      nodeYPositions.put(node, yPos);
      return yPos;
    } else {
      double sumY = 0;
      int count = 0;
      for (PhylogeneticNode child : node.getChildren()) {
        sumY += calculateNodePositions(child);
        count++;
      }
      double yPos = sumY / count;
      nodeYPositions.put(node, yPos);
      return yPos;
    }
  }
  
  /**
   * Draw the dendrogram lines.
   */
  private void drawDendrogramLines(PhylogeneticNode node) {
    if (!node.isLeaf()) {
      double nodeX = node.getHeight();
      double nodeY = nodeYPositions.get(node);
      
      for (PhylogeneticNode child : node.getChildren()) {
        double childX = child.getHeight();
        double childY = nodeYPositions.get(child);
        
        // Create a series for this branch
        XYSeries branch = new XYSeries("Branch" + System.nanoTime());
        
        // Horizontal line from child to parent's x position
        branch.add(childX, childY);
        branch.add(nodeX, childY);
        
        // Vertical line at parent's x position
        branch.add(nodeX, childY);
        branch.add(nodeX, nodeY);
        
        dataset.addSeries(branch);
        
        // Recursively draw child branches
        drawDendrogramLines(child);
      }
    }
  }
}