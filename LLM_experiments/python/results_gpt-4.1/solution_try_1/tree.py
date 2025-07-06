from typing import List, Optional, Dict, Set, Tuple


class TreeNode:
    def __init__(
        self,
        label: Optional[str] = None,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
        height: Optional[int] = None,
        members: Optional[Set[str]] = None,
    ):
        self.label = label
        self.left = left
        self.right = right
        self.height = height
        self.members = members if members is not None else (
            {label} if label else set()
        )

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __repr__(self):
        if self.is_leaf():
            return f"Leaf({self.label})"
        return f"Node(height={self.height}, members={self.members})"


def build_phylogenetic_tree(
    species: List[str], similarity_scores: Dict[str, int]
) -> TreeNode:
    clusters: List[TreeNode] = [
        TreeNode(label=sp, members={sp}) for sp in species
    ]

    def cluster_similarity(c1: TreeNode, c2: TreeNode) -> int:
        max_sim = None
        for sp1 in c1.members:
            for sp2 in c2.members:
                if sp1 == sp2:
                    continue
                key = (
                    f"{sp1}_{sp2}"
                    if f"{sp1}_{sp2}" in similarity_scores
                    else f"{sp2}_{sp1}"
                )
                sim = similarity_scores[key]
                if max_sim is None or sim > max_sim:
                    max_sim = sim
        return max_sim

    while len(clusters) > 1:
        max_sim = None
        pair_to_merge: Tuple[int, int] = (-1, -1)
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                sim = cluster_similarity(clusters[i], clusters[j])
                if max_sim is None or sim > max_sim:
                    max_sim = sim
                    pair_to_merge = (i, j)

        i, j = pair_to_merge
        c1, c2 = clusters[i], clusters[j]
        new_members = c1.members.union(c2.members)
        new_node = TreeNode(
            label=None,
            left=c1,
            right=c2,
            height=max_sim,
            members=new_members,
        )
        clusters = [
            clusters[k]
            for k in range(len(clusters))
            if k not in (i, j)
        ] + [new_node]

    return clusters[0]


def to_newick(node: TreeNode) -> str:
    if node.is_leaf():
        return node.label
    left = to_newick(node.left)
    right = to_newick(node.right)
    return f"({left},{right})"


def to_newick_with_distances(node: TreeNode, parent_height: Optional[int] = None) -> str:
    if node.is_leaf():
        branch_length = parent_height if parent_height is not None else 0
        return f"{node.label}:{int(branch_length)}"
    left = to_newick_with_distances(node.left, node.height)
    right = to_newick_with_distances(node.right, node.height)
    if parent_height is not None:
        branch_length = parent_height - node.height
        return f"({left},{right}):{int(branch_length)}"
    else:
        return f"({left},{right})"


def get_clusters_below_threshold(
    node: TreeNode, threshold: int
) -> List[List[str]]:
    clusters = []

    def collect_leaves(n: TreeNode) -> List[str]:
        if n.is_leaf():
            return [n.label]
        return collect_leaves(n.left) + collect_leaves(n.right)

    def traverse(n: TreeNode):
        if n.height is None or n.height < threshold:
            clusters.append(collect_leaves(n))
        else:
            if n.left:
                traverse(n.left)
            if n.right:
                traverse(n.right)

    traverse(node)
    return clusters