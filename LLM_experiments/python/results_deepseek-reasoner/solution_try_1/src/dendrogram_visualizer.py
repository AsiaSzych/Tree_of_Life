import matplotlib.pyplot as plt
from tree_node import TreeNode

class DendrogramVisualizer:
    def __init__(self):
        self.leaf_count = 0
        self.leaf_positions = {}
        self.max_similarity = 0
    
    def _assign_leaf_positions(self, node: TreeNode):
        if node.name is not None:
            self.leaf_positions[node] = self.leaf_count
            self.leaf_count += 1
            return [node]
        left_leaves = self._assign_leaf_positions(node.left)
        right_leaves = self._assign_leaf_positions(node.right)
        return left_leaves + right_leaves
    
    def _plot_node(self, node: TreeNode, ax):
        if node.name is not None:
            return self.leaf_positions[node], node.height
        
        left_y, left_x = self._plot_node(node.left, ax)
        right_y, right_x = self._plot_node(node.right, ax)
        node_y = (left_y + right_y) / 2
        node_x = node.height
        self.max_similarity = max(self.max_similarity, node_x)
        
        ax.plot([left_x, node_x], [left_y, left_y], 'b-', linewidth=1.5)
        ax.plot([right_x, node_x], [right_y, right_y], 'b-', linewidth=1.5)
        ax.plot([node_x, node_x], [left_y, right_y], 'b-', linewidth=1.5)
        return node_y, node_x
    
    def plot(self, root: TreeNode, filename: str):
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
        self.leaf_count = 0
        self.leaf_positions = {}
        self.max_similarity = 0
        
        all_leaves = self._assign_leaf_positions(root)
        self._plot_node(root, ax)
        
        leaf_labels = [leaf.name for leaf in all_leaves]
        leaf_positions = [self.leaf_positions[leaf] for leaf in all_leaves]
        plt.yticks(leaf_positions, leaf_labels)
        
        plt.xlabel("Needleman-Wunsch Similarity Score")
        plt.title("Phylogenetic Tree Dendrogram")
        plt.xlim(0, self.max_similarity * 1.05)
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"Saved dendrogram to {filename}")