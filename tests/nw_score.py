import argparse 
import json
from pprint import pprint

def read_file(path: str) -> dict:
    with open(path) as input_file:
        return json.load(input_file)


def compare_dicts(expected: dict, actual: dict):
    differences = {}
    for k_expected in expected:
        if k_expected in actual and actual[k_expected] != expected[k_expected]:
            differences[k_expected] = {'expected': expected[k_expected], 'actual': actual[k_expected]} 
        elif k_expected not in actual:
            differences[k_expected] = {'expected': expected[k_expected], 'actual': 'missing'}
    
    for k_actual in actual:
        if k_actual not in expected:
            differences[k_actual] = {'expected': 'missing', 'actual': actual[k_actual]}

    return differences


def main():
    parser = argparse.ArgumentParser(description='Needleman-Wunsch scores compoarator. Gets two JSON files with the ogranisms paris and their scores and compare them with each other.')
    parser.add_argument('-e', '--expected', help='JSON file with the expected results for organisms pairs and their scores.', required=True)
    parser.add_argument('-a', '--actual', nargs='+', help='JSON file wit the actual results that will be tested against the baseline. You can pass multiple files to compare all of them with the expected one', required=True)
    args = parser.parse_args()

    expected = read_file(args.expected)
    
    passed = 0
    failed = 0

    for actual_input in args.actual:
        actual = read_file(actual_input)
        
        print('----------------------------------')
        print(f'Comparing expected {args.expected} with actual {actual_input}')
        differences = compare_dicts(expected, actual)

        if differences:
            print('The scores are not the same!')
            pprint(differences, sort_dicts=False)
            failed += 1
        else:
            print("Correct")
            passed += 1
        print('----------------------------------')
    print("--- Summary ---")
    print(f'Passed: {passed}; Failed: {failed}; Total: {passed + failed}')

if __name__ == "__main__":
    main()
