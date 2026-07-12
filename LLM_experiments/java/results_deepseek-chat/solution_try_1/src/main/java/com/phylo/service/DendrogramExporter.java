package com.phylo.service;

import com.phylo.model.ClusterNode;
import org.jfree.chart.*;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;

import java.awt.*;
import java.io.File;
import java.io.IOException;
import org.jfree.chart.ChartUtils;

/**
 * Handles dendrogram visualization and export.
 */
public class DendrogramExporter {

    public static void exportDendrogram(ClusterNode root, String blosumType) 
            throws IOException {
        DefaultCategoryDataset dataset = buildDataset(root);
        JFreeChart chart = createChart(dataset, "Phylogenetic Tree (BLOSUM" + blosumType + ")");
        
        File file = new File("./phylogenetic_tree_blosum" + blosumType + ".png");
        ChartUtils.saveChartAsPNG(file, chart, 1200, 800);
    }

    private static DefaultCategoryDataset buildDataset(ClusterNode node) {
        DefaultCategoryDataset dataset = new DefaultCategoryDataset();
        addNodeToDataset(dataset, node, "Root");
        return dataset;
    }

    private static void addNodeToDataset(DefaultCategoryDataset dataset, 
                                       ClusterNode node, String series) {
        if (node.isLeaf()) {
            dataset.addValue(node.getHeight(), series, node.getLabel());
        } else {
            addNodeToDataset(dataset, node.getLeft(), series);
            addNodeToDataset(dataset, node.getRight(), series);
            dataset.addValue(node.getHeight(), series, 
                           "Node_" + node.getLabel().hashCode());
        }
    }

    private static JFreeChart createChart(DefaultCategoryDataset dataset, String title) {
        CategoryAxis domainAxis = new CategoryAxis("Species");
        domainAxis.setTickMarksVisible(false);
        
        NumberAxis rangeAxis = new NumberAxis("Similarity Score");
        rangeAxis.setStandardTickUnits(NumberAxis.createIntegerTickUnits());
        
        CategoryPlot plot = new CategoryPlot(
            dataset, 
            domainAxis, 
            rangeAxis, 
            new DendrogramRenderer()
        );
        plot.setOrientation(PlotOrientation.HORIZONTAL);
        
        JFreeChart chart = new JFreeChart(
            title,
            new Font("SansSerif", Font.BOLD, 16),
            plot,
            false
        );
        
        chart.setBackgroundPaint(Color.WHITE);
        return chart;
    }
}