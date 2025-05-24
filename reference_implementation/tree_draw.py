from ete3 import Tree, TreeStyle

newick_txt_file = "./tree62_newick_with_distance.nw"
tree_newick = ""
with open(newick_txt_file, 'r') as f:
    tree_newick = f.read()

t = Tree(tree_newick, format=6)
ts = TreeStyle()
ts.show_leaf_name = True
ts.show_branch_length = True
t.show(tree_style=ts)
t.render("mytree.png",tree_style=ts)
