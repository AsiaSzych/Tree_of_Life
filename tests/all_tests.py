import os
from nw_score import compare_dicts
from newick_validate import check_valid_newick
from newick_compare import compare_trees
from cluster_compare import compare_clusters, read_file

BLOSUM = 62
expected_folder = "../reference_implementation"
actual_folder = "../LLM_experiments/test_results/test_solution_version_GoalInstructionOutput_v1/output"

def test_compare_needleman_wunsch_score():
    file_name = f"organisms_scores_blosum{BLOSUM}.json"
    expected_file = os.path.join(expected_folder, file_name)
    actual_file = os.path.join(actual_folder, file_name)                       
    expected_dict = read_file(expected_file)
    actual_dict = read_file(actual_file)
    assert compare_dicts(expected=expected_dict, actual=actual_dict)=={} 

def test_valid_newick_only_nodes():
    file_name = f"tree_blosum{BLOSUM}_newick.nw"
    actual_tree_file = os.path.join(actual_folder, file_name)
    assert check_valid_newick(file_path=actual_tree_file)

def test_valid_newick_with_distance():
    file_name = f"tree_blosum{BLOSUM}_newick_with_distance.nw"
    actual_tree_file = os.path.join(actual_folder, file_name)
    assert check_valid_newick(file_path=actual_tree_file)

def test_compare_trees_only_nodes():
    file_name = f"tree_blosum{BLOSUM}_newick.nw"
    expected_file = os.path.join(expected_folder, file_name)
    actual_file = os.path.join(actual_folder, file_name)    
    assert compare_trees(expected_file_path=expected_file, actual_file_path=actual_file)

def test_compare_trees_with_distance():
    file_name = f"tree_blosum{BLOSUM}_newick_with_distance.nw"
    expected_file = os.path.join(expected_folder, file_name)
    actual_file = os.path.join(actual_folder, file_name)    
    assert compare_trees(expected_file_path=expected_file, actual_file_path=actual_file)

def test_compare_clusters():
    file_name = f"clusters_for_blosum{BLOSUM}.json"
    expected_file = os.path.join(expected_folder, file_name)
    actual_file = os.path.join(actual_folder, file_name)
    expected_dict = read_file(expected_file)
    actual_dict = read_file(actual_file)
    assert compare_clusters(expected=expected_dict, actual=actual_dict)=={}

def test_check_png_file_path_exists():
    file_name = f"phylogenetic_tree_blosum{BLOSUM}.png"
    actual_file = os.path.join(actual_folder, file_name)    
    assert os.path.exists(actual_file)