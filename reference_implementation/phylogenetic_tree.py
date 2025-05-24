import json

nw_json_file_path = "./organisms_scores_blosum62.json"
organisms_json_file_path = "../starter_code/organisms.json"
newick_txt_file = "./tree62_newick.nw"

with open(nw_json_file_path, 'r') as j:
    nw_scores = json.loads(j.read())

with open(organisms_json_file_path, 'r') as j:
    organisms = json.loads(j.read())

nw_scores_sorted = {k: v for k, v in sorted(nw_scores.items(), key=lambda item: item[1], reverse=True)}


class Node:

    def __init__(self, value, parent=None, root=None, left=None, right=None):
        self.data = value
        self.left = left
        self.right = right
        self.parent = parent
        self.root = root
    
    def set_root(self, root):
        self.root = root

    def set_parent(self, parent):
        self.parent = parent

class Tree:

    def createNode(self, data, parent=None, root=None, left=None, right=None):

        return Node(data, parent=parent, root=root, left=left, right=right)

    def insert(self, node, node_data, left_child, right_child):

        #if tree is empty , return a root node
        if node is None:
            return self.createNode(data=node_data, left=left_child, right=right_child)

        return node
    
    def change_root_for_all_children(self, current_node, new_root, fast_track):
        current_node.set_parent(new_root)
        fast_track[current_node.data] = new_root
        if current_node.left:
            fast_track = self.change_root_for_all_children(current_node.left, new_root, fast_track)
        if current_node.right:
            fast_track = self.change_root_for_all_children(current_node.right, new_root, fast_track)
        
        return fast_track

    def make_newick(self, node):
        newick = ""
        newick = self.traverse_newick(node, newick)
        return f"{newick};"

    def traverse_newick(self, root_node, newick):
        if root_node.left and not root_node.right:
            newick = f"(,{self.traverse_newick(root_node.left, newick)}){root_node.data}"
        elif not root_node.left and root_node.right:
            newick = f"({self.traverse_newick(root_node.right, newick)},){root_node.data}"
        elif root_node.left and root_node.right:
            newick = f"({self.traverse_newick(root_node.right, newick)},{self.traverse_newick(root_node.left, newick)}){root_node.data}"
        elif not root_node.left and not root_node.right:
            newick = f"{root_node.data}"
        else:
            pass
        return newick

class UnionFind:
    def __init__(self, keys):
      
        # Initialize the parent array with each 
        # element as its own representative
        self.parent = {}
        for key in keys:
            self.parent[key] = key
        
    def find(self, key):
      
        # If i itself is root or representative
        if self.parent[key] == key:
            return key
          
        # Else recursively find the representative 
        # of the parent
        return self.find(self.parent[key])
    
    def unite(self, key1, key2):
      
        # Representative of set containing i
        irep = self.find(key1)
        
        # Representative of set containing j
        jrep = self.find(key2)
        
        # Make the representative of i's set
        # be the representative of j's set
        self.parent[irep] = jrep


union_find_structure = UnionFind(organisms.keys())

treeOfLife = Tree()

def init_tracking_tree(init_dict, main_tree):
    tracking_dict = {}
    keys = list(init_dict.keys())
    for key in keys:
        key_node = main_tree.createNode(data=key)
        tracking_dict[key] = key_node

    return tracking_dict

tracking_tree = init_tracking_tree(organisms, treeOfLife)

for k, v in nw_scores_sorted.items():
    species = k.split("_")
    specie1 = species[0]
    specie2 = species[1]
    species1_root_node = tracking_tree[specie1]
    species2_root_node = tracking_tree[specie2]
    species1_root = union_find_structure.find(specie1)
    species2_root = union_find_structure.find(specie2)

    if species1_root!=species2_root:
        union_find_structure.unite(specie1, specie2)
        new_parent_node = treeOfLife.createNode(data = v, left=species1_root_node, right=species2_root_node)
        tracking_tree = treeOfLife.change_root_for_all_children(current_node=species1_root_node, new_root=new_parent_node, fast_track = tracking_tree)
        tracking_tree = treeOfLife.change_root_for_all_children(current_node=species2_root_node, new_root=new_parent_node, fast_track = tracking_tree)


tree_newick = treeOfLife.make_newick(new_parent_node)
with open(newick_txt_file, 'w') as f:
    f.write(tree_newick)