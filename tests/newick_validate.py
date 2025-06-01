import argparse 
from ete3 import Tree

def check_valid_newick(file_path):
    try:
        Tree(file_path, format=0).write(format=1)
        return True
    except:
        return False


def main():
    parser = argparse.ArgumentParser(description='Validates if the files contains valid tree encoded in Newick format.')
    parser.add_argument('-t', '--tree', nargs='+', help='File with tree represented in Newick format, either with the distances or withouth them.', required=True)
    args = parser.parse_args()

    passed = 0
    failed = 0

    for tree_file in args.tree:

        if check_valid_newick(tree_file):
            print(f"[{tree_file}] -> valid")
            passed += 1
        else:
            print(f"[{tree_file}] -> not valid!")
            failed += 1
    print("--- Summary ---")
    print(f'Passed: {passed}; Failed: {failed}; Total: {passed + failed}')

if __name__ == "__main__":
    main()
