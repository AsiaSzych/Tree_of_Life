class ClusterExtractor:
    @staticmethod
    def extract_clusters(node, threshold: int):
        if node.name is not None: return [[node.name]]
        if node.height < threshold:
            left = ClusterExtractor.extract_clusters(node.left, threshold)
            right = ClusterExtractor.extract_clusters(node.right, threshold)
            return left + right
        
        left = ClusterExtractor.extract_clusters(node.left, threshold)
        right = ClusterExtractor.extract_clusters(node.right, threshold)
        return [left[0] + right[0]] if left and right else []