from typing import Dict, List, Optional, Set, Tuple

class TreeNode:
    def __init__(
        self,
        name: Optional[str] = None,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
        height: Optional[int] = None,
        members: Optional[Set[str]] = None,
    ):
        self.name = name
        self.left = left
        self.right = right
        self.height = height
        self.members = members if members is not None else set()
        if self.name:
            self.members.add(self.name)

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def __repr__(self):
        if self.is_leaf():
            return f"Leaf({self.name})"
        return f"Node(height={self.height}, members={self.members})"

def build_phylogenetic_tree(
    similarity_scores: Dict[str, int], species: List[str]
) -> TreeNode:
    clusters: Dict[str, TreeNode] = {
        sp: TreeNode(name=sp) for sp in species
    }
    cluster_members: Dict[frozenset, TreeNode] = {
        frozenset([sp]): clusters[sp] for sp in species
    }
    import heapq
    heap: List[Tuple[int, frozenset, frozenset]] = []
    for i, sp1 in enumerate(species):
        for j, sp2 in enumerate(species):
            if j <= i:
                continue
            key = f"{sp1}_{sp2}"
            sim = similarity_scores[key]
            heapq.heappush(heap, (-sim, frozenset([sp1]), frozenset([sp2])))
    active_clusters: Set[frozenset] = set(cluster_members.keys())
    while len(active_clusters) > 1:
        while True:
            if not heap:
                raise RuntimeError("Heap exhausted before tree complete.")
            neg_sim, c1, c2 = heapq.heappop(heap)
            if c1 in active_clusters and c2 in active_clusters:
                break
        sim = -neg_sim
        left = cluster_members[c1]
        right = cluster_members[c2]
        merged_members = c1.union(c2)
        new_node = TreeNode(
            name=None,
            left=left,
            right=right,
            height=sim,
            members=set(merged_members),
        )
        active_clusters.remove(c1)
        active_clusters.remove(c2)
        active_clusters.add(frozenset(merged_members))
        cluster_members[frozenset(merged_members)] = new_node
        for other in active_clusters:
            if other == frozenset(merged_members):
                continue
            max_sim = None
            for m1 in merged_members:
                for m2 in other:
                    if m1 == m2:
                        continue
                    k1 = f"{m1}_{m2}"
                    k2 = f"{m2}_{m1}"
                    s = similarity_scores.get(k1, similarity_scores.get(k2))
                    if s is not None:
                        if (max_sim is None) or (s > max_sim):
                            max_sim = s
            if max_sim is not None:
                heapq.heappush(
                    heap,
                    (-max_sim, frozenset(merged_members), other),
                )
    root_key = next(iter(active_clusters))
    return cluster_members[root_key]