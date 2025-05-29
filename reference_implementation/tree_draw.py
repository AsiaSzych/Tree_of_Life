from ete3 import Tree, TreeStyle

BLOSUM_VERSION = 50
DISTANCE="_with_distance"

if DISTANCE == "":
    NEWICK_FORMAT=8
elif DISTANCE=="_with_distance":
    NEWICK_FORMAT=6
else:
    NEWICK_FORMAT=1

newick_txt_file = f"./tree{BLOSUM_VERSION}_newick{DISTANCE}.nw"
tree_newick = ""
with open(newick_txt_file, 'r') as f:
    tree_newick = f.read()

t = Tree(tree_newick, format=NEWICK_FORMAT)
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_length = True
t.show(tree_style=ts)
t.render(f"phylogenetic_tree_{BLOSUM_VERSION}{DISTANCE}.png",tree_style=ts)
