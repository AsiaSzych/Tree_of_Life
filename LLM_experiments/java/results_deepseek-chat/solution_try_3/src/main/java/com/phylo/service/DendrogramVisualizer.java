package com.phylo.service;

import com.phylo.model.PhylogeneticNode;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartUtils;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

public class DendrogramVisualizer {
    private static final int WIDTH = 1200;
    private static final int HEIGHT = 800;
    private static final String TITLE = "Phylogenetic Tree (BLOSUM%s)";

    public static void visualize(PhylogeneticNode root, String blosumType) throws IOException {
        DefaultCategoryDataset dataset = createDataset(root);
        JFreeChart chart = ChartFactory.createBarChart(
                String.format(TITLE, blosumType),
                "Species",
                "Similarity Score",
                dataset,
                PlotOrientation.HORIZONTAL,
                false, true, false
        );

        // Customize chart appearance
        chart.getCategoryPlot().getRangeAxis().setInverted(true);
        chart.getCategoryPlot().setRenderer(new DendrogramRenderer());

        // Save to PNG
        String filename = "./phylogenetic_tree_blosum" + blosumType + ".png";
        ChartUtils.saveChartAsPNG(new File(filename), chart, WIDTH, HEIGHT);
    }

    private static DefaultCategoryDataset createDataset(PhylogeneticNode root) {
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        Map<String, Double> leafPositions = new HashMap<>();
        calculateLeafPositions(root, leafPositions);
        addDatasetEntries(root, dataset, leafPositions);
        return dataset;
    }

    private static void calculateLeafPositions(PhylogeneticNode node, Map<String, Double> positions) {
        if (node.isLeaf()) {
            positions.put(node.getName(), (double) positions.size());
        } else {
            for (PhylogeneticNode child : node.getChildren()) {
                calculateLeafPositions(child, positions);
            }
        }
    }

    private static void addDatasetEntries(PhylogeneticNode node, 
                                       DefaultCategoryDataset dataset,
                                       Map<String, Double> leafPositions) {
        if (!node.isLeaf()) {
            for (PhylogeneticNode child : node.getChildren()) {
                // Add vertical line
                double minPos = leafPositions.values().stream().min(Double::compare).orElse(0.0);
                double maxPos = leafPositions.values().stream().max(Double::compare).orElse(0.0);
                dataset.addValue((Number)node.getHeight(), "Node", (minPos + maxPos) / 2);
                
                // Add horizontal line

                dataset.addValue((Number)child.getHeight(), "Node", minPos);
                dataset.addValue((Number)child.getHeight(), "Node", maxPos);
                
                addDatasetEntries(child, dataset, leafPositions);
            }
        }
    }
}