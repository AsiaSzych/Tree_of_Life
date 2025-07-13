package com.phylo.service;

import org.jfree.chart.renderer.category.BarRenderer;
import org.jfree.data.category.CategoryDataset;

import java.awt.*;

public class DendrogramRenderer extends BarRenderer {
    @Override
    public Paint getItemPaint(int row, int column) {
        return Color.BLACK; // All lines black
    }

    @Override
    public Stroke getItemStroke(int row, int column) {
        return new BasicStroke(2.0f); // Thicker lines
    }

    @Override
    public double getItemMargin() {
        return 0; // No margin between items
    }
}