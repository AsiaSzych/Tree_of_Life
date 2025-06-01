import argparse 
import json
from pprint import pprint

def read_file(path: str) -> dict:
    with open(path) as input_file:
        return json.load(input_file)


def compare_clusters(expected: dict, actual: dict):
    differences = {}

    for threshold in expected:

        # completely missing key
        if threshold not in actual:
            differences[threshold] = {'actual': 'missing results for the threhold'}
            continue

        # clusters comparison
        expected_clusters = {frozenset(cluster) for cluster in expected[threshold]}
        actual_clusters = {frozenset(cluster) for cluster in actual[threshold]}

        missing_clusters = expected_clusters - actual_clusters
        extra_clusters = actual_clusters - expected_clusters

        if missing_clusters or extra_clusters:
            differences[threshold] = {}

            if missing_clusters:
                differences[threshold]['missing_clusters'] = [
                    sorted(list(cluster)) for cluster in missing_clusters
                ]
            if extra_clusters:
                differences[threshold]['unexpected_clusters'] = [
                    sorted(list(cluster)) for cluster in extra_clusters
                ]

            # partial overlaps
            diffs = []
            for m in missing_clusters:
                for u in extra_clusters:
                    if m & u:  # shared elements
                        diffs.append({
                            'expected_cluster': sorted(m),
                            'actual_cluster': sorted(u),
                            'missing_elements': sorted(list(m - u)),
                            'unexpected_elements': sorted(list(u - m))
                        })
            if diffs:
                differences[threshold]['partial_matches'] = diffs

    for threshold in actual:
        if threshold not in expected:
            differences[threshold] = {'expected': 'found threshold results that is not expected'}

    return differences


def main():
    parser = argparse.ArgumentParser(description='Clusters compoarator. Gets two files with the clusters in JSON format and compare them with each other.')
    parser.add_argument('-e', '--expected', help='JSON file with the expected cluster.', required=True)
    parser.add_argument('-a', '--actual', nargs='+', help='JSON file wit the actual cluster that will be tested against the base one. You can pass multiple files to compare all of them with the expected one', required=True)
    args = parser.parse_args()

    expected = read_file(args.expected)

    passed = 0
    failed = 0

    for actual_input in args.actual:
        actual = read_file(actual_input)
        
        print('----------------------------------')
        print(f'Comparing expected {args.expected} with actual {actual_input}')
        differences = compare_clusters(expected, actual)
        if differences:
            pprint(differences, sort_dicts=False)
            failed += 1
        else:
            print("Clusters are the same!")
            passed += 1
        
        print('----------------------------------')
    print("--- Summary ---")
    print(f'Passed: {passed}; Failed: {failed}; Total: {passed + failed}')

if __name__ == "__main__":
    main()