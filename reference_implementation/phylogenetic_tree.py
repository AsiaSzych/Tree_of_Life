import json
BLOSUM_VERSION = 50

nw_json_file_path = f"./organisms_scores_blosum{BLOSUM_VERSION}.json"
organisms_json_file_path = "../starter_code/organisms.json"
newick_txt_file = f"./tree_blosum{BLOSUM_VERSION}_newick.nw"
newick_distance_txt_file = f"./tree_blosum{BLOSUM_VERSION}_newick_with_distance.nw"
thresholds_file_path=  "../starter_code/thresholds.txt"
clusters_output_path = f"./clusters_for_blosum{BLOSUM_VERSION}.json"


class Node:

    def __init__(self, name, value, parent=None, root=None, left=None, right=None, is_leaf=False):
        self.name = name
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.root = root
        self.is_leaf = is_leaf
    
    def set_root(self, root):
        self.root = root

    def set_parent(self, parent):
        self.parent = parent

    def update_distance(self, distance):
        self.distance = distance

class Tree:

    def createNode(self, name, value, parent=None, root=None, left=None, right=None, is_leaf=False):

        return Node(name=name, value=value, parent=parent, root=root, left=left, right=right, is_leaf=is_leaf)

    def insert(self, node, node_name, node_value, left_child, right_child):

        if node is None:
            return self.createNode(name=node_name, value=node_value, left=left_child, right=right_child)

        return node
    
    def change_root_for_all_children(self, current_node, new_root, fast_track):

        current_node.set_parent(new_root)
        fast_track[current_node.name] = new_root
        if current_node.left:
            fast_track = self.change_root_for_all_children(current_node.left, new_root, fast_track)
        if current_node.right:
            fast_track = self.change_root_for_all_children(current_node.right, new_root, fast_track)
        
        return fast_track

    def make_newick(self, node, distance=False):

        newick = ""
        if distance:
            newick = self.traverse_newick_with_distance(node, newick)
        else:
            newick = self.traverse_newick(node, newick)
        return f"{newick};"
    
    def traverse_newick(self, root_node, newick):

        if root_node.left and not root_node.right:
            newick = f"(,{self.traverse_newick(root_node.left, newick)}){root_node.name}"
        elif not root_node.left and root_node.right:
            newick = f"({self.traverse_newick(root_node.right, newick)},){root_node.name}"
        elif root_node.left and root_node.right:
            newick = f"({self.traverse_newick(root_node.right, newick)},{self.traverse_newick(root_node.left, newick)}){root_node.name}"
        elif not root_node.left and not root_node.right:
            newick = f"{root_node.name}"
        else:
            pass
        return newick

    def traverse_newick_with_distance(self, root_node, newick):

        if root_node.left and not root_node.right:
            newick = f"(,{self.traverse_newick_with_distance(root_node.left, newick)}):{root_node.distance}"
        elif not root_node.left and root_node.right:
            newick = f"({self.traverse_newick_with_distance(root_node.right, newick)},):{root_node.distance}"
        elif root_node.left and root_node.right:
            newick = f"({self.traverse_newick_with_distance(root_node.right, newick)},{self.traverse_newick_with_distance(root_node.left, newick)}):{root_node.distance}"
        elif not root_node.left and not root_node.right:
            newick = f"{root_node.name}:{root_node.distance}"
        else:
            pass
        return newick

class UnionFind:
    def __init__(self, keys):

        self.parent = {}
        for key in keys:
            self.parent[key] = key
        
    def find(self, key):

        if self.parent[key] == key:
            return key
          
        return self.find(self.parent[key])
    
    def unite(self, key1, key2):
      
        # Representative of set containing i
        irep = self.find(key1)
        
        # Representative of set containing j
        jrep = self.find(key2)
        
        # Make the representative of i's set
        # be the representative of j's set
        self.parent[irep] = jrep


def init_tracking_cache(init_dict:dict, main_tree:Tree, nw_scores_sorted:dict):

    max_distance = nw_scores_sorted[list(nw_scores_sorted.keys())[0]]
    # max_distance = max_distance + 50
    tracking_dict = {}
    keys = list(init_dict.keys())
    for key in keys:
        key_node = main_tree.createNode(name=key, value=max_distance, is_leaf=True)
        key_node.update_distance(max_distance)
        tracking_dict[key] = key_node

    return tracking_dict



def create_tree(tree:Tree, nw_scores_sorted:dict, tracking_cache:dict, union_find:UnionFind):
    node_counter = 1
    for k, v in nw_scores_sorted.items():
        species = k.split("_")
        specie1 = species[0]
        specie2 = species[1]
        species1_root_node:Node = tracking_cache[specie1]
        species2_root_node:Node= tracking_cache[specie2]
        species1_root = union_find.find(specie1)
        species2_root = union_find.find(specie2)

        if species1_root!=species2_root:
            union_find.unite(specie1, specie2)
            node_counter = node_counter+1
            new_parent_node = tree.createNode(name = '', value = v, left=species1_root_node, right=species2_root_node)
            species1_root_node.update_distance(species1_root_node.value - new_parent_node.value)
            species2_root_node.update_distance(species2_root_node.value - new_parent_node.value)
            tracking_cache = tree.change_root_for_all_children(current_node=species1_root_node, new_root=new_parent_node, fast_track = tracking_cache)
            tracking_cache = tree.change_root_for_all_children(current_node=species2_root_node, new_root=new_parent_node, fast_track = tracking_cache)
    new_parent_node.update_distance(0)
    return tree, new_parent_node, tracking_cache, union_find

def get_leaf_nodes(root):
    if root.is_leaf:
        return [root.name]

    my_leafs = []

    if root.left:
        my_leafs = my_leafs + get_leaf_nodes(root.left)

    if root.right:
        my_leafs  = my_leafs + get_leaf_nodes(root.right)

    return my_leafs


def generate_clusters(tree_root:Node, threshold:int, all_clusters:list):
    if not tree_root:
        return
    elif tree_root.value < threshold:
        #If the threshold is not exceeded iteratively look starting from children
        generate_clusters(tree_root.left, threshold, all_clusters)
        generate_clusters(tree_root.right, threshold, all_clusters)
    else:
        # If the threshold is exceeded, create cluster starting from that node
        cluster = get_leaf_nodes(tree_root)
        all_clusters.append(cluster)
    return all_clusters

if __name__ == "__main__":

    with open(nw_json_file_path, 'r') as j:
        nw_scores = json.loads(j.read())

    with open(organisms_json_file_path, 'r') as j:
        organisms = json.loads(j.read())

    nw_scores_sorted = {k: v for k, v in sorted(nw_scores.items(), key=lambda item: item[1], reverse=True)}
    union_find_structure = UnionFind(organisms.keys())
    tree_of_life = Tree()
    tracking_cache = init_tracking_cache(organisms, tree_of_life, nw_scores_sorted)

    tree_of_life, root, tracking_cache, union_find_structure = create_tree(tree_of_life, nw_scores_sorted, tracking_cache, union_find_structure)

    tree_newick = tree_of_life.make_newick(root)
    tree_newick_with_distance = tree_of_life.make_newick(root, distance=True)

    with open(newick_txt_file, 'w') as f:
        f.write(tree_newick)
    with open(newick_distance_txt_file, 'w') as f:
        f.write(tree_newick_with_distance)


    with open(thresholds_file_path, 'r') as f:
        thresholds = [int(line) for line in f]

    clusters_dict = {}
    for threshold in thresholds:
        clusters = generate_clusters(root, threshold, [])
        clusters_dict[threshold] = clusters

    with open(clusters_output_path, 'w') as j:
        json.dump(clusters_dict, j)