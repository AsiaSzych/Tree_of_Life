class TreeSerializer:
    @staticmethod
    def to_simple_newick(node) -> str:
        if node.name is not None: return node.name
        left_str = TreeSerializer.to_simple_newick(node.left)
        right_str = TreeSerializer.to_simple_newick(node.right)
        return f"({left_str},{right_str})"

    @staticmethod
    def to_distance_newick(node, parent_height: int = None) -> str:
        branch_len = abs(parent_height - node.height) if parent_height else 0
        if node.name is not None: return f"{node.name}:{int(branch_len)}"
        
        left_str = TreeSerializer.to_distance_newick(node.left, node.height)
        right_str = TreeSerializer.to_distance_newick(node.right, node.height)
        subtree = f"({left_str},{right_str})"
        return subtree + f":{int(branch_len)}" if branch_len > 0 else subtree