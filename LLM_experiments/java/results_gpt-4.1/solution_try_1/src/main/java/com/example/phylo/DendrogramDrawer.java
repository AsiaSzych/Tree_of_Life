package com.example.phylo;

import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import javax.imageio.ImageIO;

public class DendrogramDrawer {

  private static final int IMAGE_WIDTH = 1200;
  private static final int IMAGE_HEIGHT = 40;
  private static final int MARGIN_LEFT = 120;
  private static final int MARGIN_RIGHT = 40;
  private static final int MARGIN_TOP = 40;
  private static final int MARGIN_BOTTOM = 40;
  private static final int VERTICAL_SPACING = 40;
  private static final int LABEL_OFFSET = 8;

  public static void drawDendrogram(PhyloNode root, String filePath) throws IOException {
    List<String> leaves = root.getAllSpecies();
    int nLeaves = leaves.size();
    int height = Math.max(IMAGE_HEIGHT * nLeaves / 4, 200);

    int minHeight = 0;
    int maxHeight = getMaxHeight(root);

    BufferedImage image = new BufferedImage(IMAGE_WIDTH, height, BufferedImage.TYPE_INT_ARGB);
    Graphics2D g = image.createGraphics();
    g.setColor(Color.WHITE);
    g.fillRect(0, 0, IMAGE_WIDTH, height);

    g.setColor(Color.BLACK);
    g.setStroke(new BasicStroke(2));
    g.setFont(new Font("Arial", Font.PLAIN, 16));

    Map<String, Integer> leafY = new HashMap<>();
    for (int i = 0; i < leaves.size(); i++) {
      int y = MARGIN_TOP + i * VERTICAL_SPACING;
      leafY.put(leaves.get(i), y);
    }

    drawNode(g, root, minHeight, maxHeight, leafY, filePath);

    g.dispose();
    ImageIO.write(image, "png", new File(filePath));
  }

  private static int drawNode(Graphics2D g, PhyloNode node, int minHeight, int maxHeight, Map<String, Integer> leafY, String filePath) {
    if (node.isLeaf()) {
      int x = toX(0, minHeight, maxHeight);
      int y = leafY.get(node.getName());
      g.drawString(node.getName().replace(' ', '_'), x - LABEL_OFFSET - g.getFontMetrics().stringWidth(node.getName()), y + 5);
      return y;
    } else {
      int x = toX(node.getHeight(), minHeight, maxHeight);
      int leftY = drawNode(g, node.getLeft(), minHeight, maxHeight, leafY, filePath);
      int rightY = drawNode(g, node.getRight(), minHeight, maxHeight, leafY, filePath);

      g.drawLine(x, leftY, x, rightY);

      int leftChildX = toX(node.getLeft().isLeaf() ? 0 : node.getLeft().getHeight(), minHeight, maxHeight);
      int rightChildX = toX(node.getRight().isLeaf() ? 0 : node.getRight().getHeight(), minHeight, maxHeight);

      g.drawLine(leftChildX, leftY, x, leftY);
      g.drawLine(rightChildX, rightY, x, rightY);

      String scoreStr = Integer.toString(node.getHeight());
      g.setFont(new Font("Arial", Font.PLAIN, 12));
      g.drawString(scoreStr, x + 4, (leftY + rightY) / 2 - 4);
      g.setFont(new Font("Arial", Font.PLAIN, 16));

      return (leftY + rightY) / 2;
    }
  }

  private static int toX(int height, int minHeight, int maxHeight) {
    if (maxHeight == minHeight) return MARGIN_LEFT;
    double frac = (double) height / (double) maxHeight;
    return MARGIN_LEFT + (int) ((IMAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT) * frac);
  }

  private static int getMaxHeight(PhyloNode node) {
    if (node.isLeaf()) return 0;
    return Math.max(node.getHeight(), Math.max(getMaxHeight(node.getLeft()), getMaxHeight(node.getRight())));
  }
}