import argparse 
from ete3 import Tree

def compare_trees(expected_file_path:str, actual_file_path:str):
    expected_tree = Tree(expected_file_path)
    actual_tree = Tree(actual_file_path)

    return expected_tree.write(format=1) == actual_tree.write(format=1)

def main():
    parser = argparse.ArgumentParser(description='Newick trees compoarator. Gets two files with the trees in newick format and compare them with each other.')
    parser.add_argument('-e', '--expected', help='NW file with the expected tree.', required=True)
    parser.add_argument('-a', '--actual', nargs='+', help='NW file wit the actual tree that will be tested against the base one. You can pass multiple files to compare all of them with the expected one', required=True)
    args = parser.parse_args()

    passed = 0
    failed = 0

    expeted_input = args.expected

    for actual_input in args.actual:

        print('----------------------------------')
        print(f'Comparing expected {expeted_input} with actual {actual_input}')

        if compare_trees(expeted_input, actual_input):
            print('Trees are the same!')
            passed += 1
        else:
            print("Trees are not the same!")
            failed += 1
        print('----------------------------------')

    print("--- Summary ---")
    print(f'Passed: {passed}; Failed: {failed}; Total: {passed + failed}')

if __name__ == "__main__":
    main()
