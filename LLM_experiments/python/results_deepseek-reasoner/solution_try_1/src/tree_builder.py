import sys
from tree_node import TreeNode

class TreeBuilder:
    def __init__(self, similarity_matrix, species_list: list):
        self.similarity_matrix = similarity_matrix
        self.species_list = species_list
    
    def build_tree(self) -> TreeNode:
        clusters = [TreeNode(name=species) for species in self.species_list]
        n = len(clusters)
        
        if n == 0: return None
        if n == 1: return clusters[0]
        
        sim_dict = {}
        for i in range(n):
            for j in range(i+1, n):
                c1 = clusters[i]
                c2 = clusters[j]
                s = self.similarity_matrix.get_score(c1.name, c2.name)
                
                if c1 not in sim_dict: sim_dict[c1] = {}
                if c2 not in sim_dict: sim_dict[c2] = {}
                
                sim_dict[c1][c2] = s
                sim_dict[c2][c1] = s
        
        while len(clusters) > 1:
            max_sim = -sys.maxsize
            to_merge = None
            
            for i in range(len(clusters)):
                for j in range(i+1, len(clusters)):
                    c1 = clusters[i]
                    c2 = clusters[j]
                    current_sim = sim_dict[c1][c2]
                    
                    if current_sim > max_sim:
                        max_sim = current_sim
                        to_merge = (c1, c2, i, j)
            
            if to_merge is None: break
                
            c1, c2, i_idx, j_idx = to_merge
            new_node = TreeNode(left=c1, right=c2, height=max_sim)
            
            new_sims = {}
            for c in clusters:
                if c is c1 or c is c2: continue
                s1 = sim_dict[c][c1]
                s2 = sim_dict[c][c2]
                new_sim = max(s1, s2)
                new_sims[c] = new_sim
            
            indices = sorted([i_idx, j_idx], reverse=True)
            for idx in indices: del clusters[idx]
            
            del sim_dict[c1]
            del sim_dict[c2]
            for c in sim_dict:
                if c1 in sim_dict[c]: del sim_dict[c][c1]
                if c2 in sim_dict[c]: del sim_dict[c][c2]
            
            sim_dict[new_node] = {}
            for c, s_val in new_sims.items():
                sim_dict[new_node][c] = s_val
                sim_dict[c][new_node] = s_val
            
            clusters.append(new_node)
        
        return clusters[0]