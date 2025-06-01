import argparse 
from ete3 import Tree


def main():
    parser = argparse.ArgumentParser(description='Validates if the files contains valid tree encoded in Newick format.')
    parser.add_argument('-t', '--tree', nargs='+', help='File with tree represented in Newick format, either with the distances or withouth them.', required=True)
    args = parser.parse_args()

    passed = 0
    failed = 0

    for tree_file in args.tree:
        try:
            Tree(tree_file, format=0).write(format=1)
            print(f"[{tree_file}] -> valid")
            passed += 1
        except:
            print(f"[{tree_file}] -> not valid!")
            failed += 1
    print("--- Summary ---")
    print(f'Passed: {passed}; Failed: {failed}; Total: {passed + failed}')

if __name__ == "__main__":
    main()
