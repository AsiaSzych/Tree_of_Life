package com.phylo.service;

import org.jfree.chart.renderer.category.BarRenderer;
import java.awt.*;
import java.awt.geom.Line2D;
import java.awt.geom.Rectangle2D;
import org.jfree.chart.axis.CategoryAxis;
import org.jfree.chart.axis.ValueAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.renderer.category.CategoryItemRendererState;

/**
 * Custom renderer for horizontal dendrogram visualization.
 */
public class DendrogramRenderer extends BarRenderer {
    @Override
    public void drawItem(Graphics2D g2, CategoryItemRendererState state,
                        Rectangle2D dataArea, CategoryPlot plot, 
                        CategoryAxis domainAxis, ValueAxis rangeAxis,
                        org.jfree.data.category.CategoryDataset dataset,
                        int row, int column, int pass) {
        
        Number value = dataset.getValue(row, column);
        if (value == null) return;

        double x = rangeAxis.valueToJava2D(value.doubleValue(), dataArea, 
                                         plot.getRangeAxisEdge());
        double y = domainAxis.getCategoryMiddle(column, 
                plot.getCategoriesForAxis(domainAxis).size(), 
                dataArea, plot.getDomainAxisEdge());

        // Draw horizontal line
        g2.setPaint(Color.BLACK);
        g2.setStroke(new BasicStroke(2));
        g2.draw(new Line2D.Double(
            rangeAxis.valueToJava2D(0, dataArea, plot.getRangeAxisEdge()),
            y,
            x,
            y
        ));

        // Draw vertical connector
        if (row > 0) {
            double prevY = domainAxis.getCategoryMiddle(column, 
                    plot.getCategoriesForAxis(domainAxis).size(), 
                    dataArea, plot.getDomainAxisEdge());
            g2.draw(new Line2D.Double(x, prevY, x, y));
        }
    }
}