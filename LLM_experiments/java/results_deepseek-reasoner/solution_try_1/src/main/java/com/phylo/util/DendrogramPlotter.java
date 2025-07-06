package com.phylo.util;

import com.phylo.model.PhyloNode;
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
import java.util.Map;

public class DendrogramPlotter {
    
    public static void plotDendrogram(PhyloNode root, String blosumType) throws IOException {
        // Create dataset and collect coordinates
        XYSeriesCollection dataset = new XYSeriesCollection();
        Map<PhyloNode, double[]> coordinates = new HashMap<>();
        XYSeries branches = new XYSeries("Branches");
        
        // Calculate coordinates recursively
        calculateCoordinates(root, 0, coordinates, new double[]{0}, new int[]{0});
        
        // Collect line segments
        collectLineSegments(root, coordinates, branches);
        
        dataset.addSeries(branches);
        
        // Create chart
        JFreeChart chart = ChartFactory.createXYLineChart(
            "Phylogenetic Tree (BLOSUM" + blosumType + ")",
            "Needleman-Wunsch Similarity Score",
            "",
            dataset,
            PlotOrientation.HORIZONTAL,
            false,
            true,
            false
        );
        
        // Customize plot
        XYPlot plot = chart.getXYPlot();
        plot.setBackgroundPaint(Color.WHITE);
        plot.setRangeGridlinePaint(Color.LIGHT_GRAY);
        plot.setDomainGridlinePaint(Color.LIGHT_GRAY);
        
        // Customize renderer
        XYLineAndShapeRenderer renderer = new XYLineAndShapeRenderer(true, false);
        renderer.setSeriesPaint(0, Color.BLUE);
        renderer.setSeriesStroke(0, new BasicStroke(1.5f));
        plot.setRenderer(renderer);
        
        // Set fixed range for y-axis
        NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
        rangeAxis.setRange(0, coordinates.size() * 2);
        rangeAxis.setVisible(false);  // Hide y-axis as per requirement
        
        // Save to file
        String fileName = "phylogenetic_tree_blosum" + blosumType + ".png";
        ChartUtils.saveChartAsPNG(new File(fileName), chart, 1200, 800);
    }

    private static void calculateCoordinates(PhyloNode node, double parentX, 
                                            Map<PhyloNode, double[]> coordinates, 
                                            double[] currentY, int[] leafCount) {
        if (node == null) return;
        
        double x = node.getHeight();
        double y;
        
        if (node.isLeaf()) {
            y = leafCount[0] * 2;  // Space leaves evenly
            leafCount[0]++;
        } else {
            // Process children first to get their positions
            calculateCoordinates(node.getLeft(), x, coordinates, currentY, leafCount);
            double leftY = coordinates.get(node.getLeft())[1];
            
            calculateCoordinates(node.getRight(), x, coordinates, currentY, leafCount);
            double rightY = coordinates.get(node.getRight())[1];
            
            y = (leftY + rightY) / 2;
        }
        
        coordinates.put(node, new double[]{x, y});
    }

    private static void collectLineSegments(PhyloNode node, 
                                           Map<PhyloNode, double[]> coordinates,
                                           XYSeries series) {
        if (node == null) return;
        
        double[] nodeCoords = coordinates.get(node);
        double nodeX = nodeCoords[0];
        double nodeY = nodeCoords[1];
        
        // Add current node position
        series.add(nodeX, nodeY);
        
        if (!node.isLeaf()) {
            // Add connection to left child
            double[] leftCoords = coordinates.get(node.getLeft());
            series.add(leftCoords[0], leftCoords[1]);
            series.add(nodeX, nodeY);  // Return to node
            
            // Add connection to right child
            double[] rightCoords = coordinates.get(node.getRight());
            series.add(rightCoords[0], rightCoords[1]);
            series.add(nodeX, nodeY);  // Return to node
            
            // Add horizontal connection between children
            series.add(nodeX, leftCoords[1]);
            series.add(nodeX, rightCoords[1]);
            series.add(nodeX, nodeY);  // Return to node
        }
        
        // Process children recursively
        collectLineSegments(node.getLeft(), coordinates, series);
        collectLineSegments(node.getRight(), coordinates, series);
    }
}