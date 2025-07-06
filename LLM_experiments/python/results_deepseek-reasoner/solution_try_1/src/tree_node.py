class TreeNode:
    def __init__(self, name: str = None, left: 'TreeNode' = None, 
                 right: 'TreeNode' = None, height: float = 0.0):
        self.name = name
        self.left = left
        self.right = right
        self.height = height