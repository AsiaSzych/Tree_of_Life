# Compare Needleman-Wush scores

### Input
2 paths to json files - reference file and testing file, both contaiing calculated Needleman-Wush scores for all pair of organisms.

### Input format 
{
    "Wild boar_Horse": 1718,
    "Wild boar_White-tailed deer": 1710, 
    "Wild boar_Reindeer": 1707, 
    "Wild boar_Domestic Yak": 1713
}
Examplary file: `../reference_implementation/organisms_scores_blosum62.json`


### Task
Check if testing file contains all the same records as reference file. Both key and values need to match. Order doesn't matter.

# Validate newick format 

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

# Compare trees based on newick

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

# Compare created clusters

### Input
2 paths to json files - reference file and testing file, both contaiing calulated cluster for given thresholds.

### Input format
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

Exemplary file: `../reference_implementation/clusters_for_blosum50.json`

### Task 
Check if testing file contains all the same records as reference file. Both key and values need to match. Order doesn't matter.