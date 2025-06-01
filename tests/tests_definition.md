# TESTS
All test that should be passed in orderd to declare implementation of the task as successfull are inlcuded in the `all_tests.py` file. This file should be run using pytest library: 
``` pytest all_tests.py```

It inlcudes 7 tests:
1. compare needleman-wush scores - described in details below in **case #1** section
2. check valid newick structure, with nodes only - described in details below in **case #2** section
3. check valid newick structure, when distances are included - described in details below in **case #2** section
4. compare two trees, with nodes only - described in details below in **case #3** section
5. compare two trees, when distances are included - described in details below in **case #3** section
6. compare clusters based on thresholds - described in details below in **case #4** section 
7. check if png file to drawing of the tree exists 


# Case #1 Compare Needleman-Wush scores

### Input
2 paths to json files - reference file and testing file, both containing calculated Needleman-Wush scores for all pair of organisms.

### Input format 
```
{
    "Wild boar_Horse": 1718,
    "Wild boar_White-tailed deer": 1710, 
    "Wild boar_Reindeer": 1707, 
    "Wild boar_Domestic Yak": 1713
}
```

Examplary file: `../reference_implementation/organisms_scores_blosum62.json`


### Task
Check if testing file contains all the same records as reference file. Both key and values need to match. Order doesn't matter.

### Script
`nw_score.py` - allows for comparing expected input with multiple actual inputs

```bash
python nw_score.py -e ../reference_implementation/organisms_scores_blosum62.json -a ../reference_implementation/organisms_scores_blosum62.json broken_blosum62.json
```
output:
```
----------------------------------
Comparing expected ../reference_implementation/organisms_scores_blosum62.json with actual ../reference_implementation/organisms_scores_blosum62.json
Correct
----------------------------------
----------------------------------
Comparing expected ../reference_implementation/organisms_scores_blosum62.json with actual broken_blosum62.json
The scores are not the same!
{'Western honeybee_Spotted Lanternfly': {'expected': 832, 'actual': 'missing'},
 'Termite_Spotted Lanternfly': {'expected': 898, 'actual': 897},
 'Random_Random': {'expected': 'missing', 'actual': 1234}}
----------------------------------
--- Summary ---
Passed: 1; Failed: 1; Total: 2
```


# Case #2 Validate newick format 

### Input 
Path to test file containg tree saved in newick format (.nw extension)

### Input format
(Black garden ant,((Asian lady beetle,(Termite,(Housefly,(Common clothes moth,Monarch butterfly)1199)1190)1185))1085,Western honeybee)832;

Examplary file: `../reference_implementation/tree62_newick.nw`

OR

(Black garden ant,((Asian lady beetle,(Termite,(Housefly,(Common clothes moth,Monarch butterfly):1199):1190):1185)):1085,Western honeybee):832;

Examplary file: `../reference_implementation/tree62_newick_with_distance.nw`

BOTH ARE VALID, TEST FUNCTON SHOULD PASS

### Task 
Check if given files contains string that represent a valid newick format. 

**Additional materials:** 
* https://en.wikipedia.org/wiki/Newick_format - definition of newick format
* https://github.com/ila/Newick-validator - tool for faster validation
* https://etetoolkit.org/docs/2.3/tutorial/tutorial_trees.html#reading-newick-trees - toolkit for working with trees, if it is possible to pass newick string to tree class it means that the string is valid, but it's important to take care of *format* parameter


### Script
`newick_validate.py` - checks if the `.nw` files are valid newick format trees
```bash
python newick_validate.py -t ../reference_implementation/tree62_newick_with_distance.nw ../reference_implementation/tree50_newick.nw
```
output
```
[../reference_implementation/tree62_newick_with_distance.nw] -> valid
[../reference_implementation/tree50_newick.nw] -> valid
--- Summary ---
Passed: 2; Failed: 0; Total: 2
``` 


# Case #3 Compare trees based on newick

### Input
2 paths to files - reference file and testing file, both containing string in newick format representing tree

### Input format
(Black garden ant,((Asian lady beetle,(Termite,(Housefly,(Common clothes moth,Monarch butterfly):1199):1190):1185)):1085,Western honeybee):832;

Examplary file: `../reference_implementation/tree62_newick_with_distance.nw`

### Task 
Compare is the trees are the same, for example if they have the same amount of nodes and the same connections between them.
(I don't have a specific way of comparison figured out yet, from what I saw there are many metrics which can be calculated) 

**Additional materials:** 
* https://etetoolkit.org/docs/2.3/tutorial/tutorial_trees.html#comparing-trees - compare method from the ete toolkit, load boths trees and run it
* https://eti.pg.edu.pl/TreeCmp/WEB - PG tool for online tree comparison

### Script
`newick_compare.py` - compare single expected tree from input `.nw` file with multiple actual input files. The comparion is made as follow:
- read newick from input
- load the tree
- compare the newick representation returned by the `ete3` library using format which prints not only the topology, but also the distances between nodes. If the input file don't have distances information, the default distance is 1. Two trees with the same topology will be different if one has information about distances and the other one doens't. 

```bash
python newick_compare.py -e ../reference_implementation/tree50_newick.nw -a ../reference_implementation/tree50_newick.nw ../reference_implementation/tree62_newick.nw ../reference_implementation/tree50_newick_with_distance.nw
```
output
```
----------------------------------
Comparing expected ../reference_implementation/tree50_newick.nw with actual ../reference_implementation/tree50_newick.nw
Trees are the same!
----------------------------------
----------------------------------
Comparing expected ../reference_implementation/tree50_newick.nw with actual ../reference_implementation/tree62_newick.nw
Trees are not the same!
----------------------------------
----------------------------------
Comparing expected ../reference_implementation/tree50_newick.nw with actual ../reference_implementation/tree50_newick_with_distance.nw
Trees are not the same!
----------------------------------
--- Summary ---
Passed: 1; Failed: 2; Total: 3
```


# Case #4 Compare created clusters

### Input
2 paths to json files - reference file and testing file, both contaiing calulated cluster for given thresholds.

### Input format
```
{
    "1100": [
        [
            "Western honeybee"
        ],
        [
            "Chameleon",
            "Bearded Dragon"
        ],
        [
            "Monarch butterfly",
            "Common clothes moth",
            "Housefly",
            "Termite"
        ]
    ],
    "1260": [
        [
            "Western honeybee"
        ],
        [
            "Russels viper"
        ],
        [
            "American alligator"
        ]
    ]
}
```

Exemplary file: `../reference_implementation/clusters_for_blosum50.json`

### Task 
Check if testing file contains all the same records as reference file. Both key and values need to match. Order doesn't matter.

### Script
`cluster_compare.py` - compares one exepcted input file with many actual files and prints detailed comparison results if two files are not the same (the order of clusters or elements in clusters are ignored).
```bash
python cluster_compare.py --expected ../reference_implementation/clusters_for_blosum50.json --actual ./broken_cluster.json ../reference_implementation/clusters_for_blosum50.json
```
output
```
----------------------------------
Comparing expected ../reference_implementation/clusters_for_blosum50.json with actual ./broken_cluster.json
{'1100': {'missing_clusters': [['Western honeybee']],
          'unexpected_clusters': [['RANDOM', 'Western honeybee']],
          'partial_matches': [{'expected_cluster': ['Western honeybee'],
                               'actual_cluster': ['RANDOM', 'Western honeybee'],
                               'missing_elements': [],
                               'unexpected_elements': ['RANDOM']}]},
 '1260': {'missing_clusters': [['Western honeybee']]},
 '1350': {'actual': 'missing results for the threhold'},
 '1234': {'expected': 'found threshold results that is not expected'}}
----------------------------------
----------------------------------
Comparing expected ../reference_implementation/clusters_for_blosum50.json with actual ../reference_implementation/clusters_for_blosum50.json
Clusters are the same!
----------------------------------
--- Summary ---
Passed: 1; Failed: 1; Total: 2
```