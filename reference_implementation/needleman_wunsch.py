import json
import numpy as np
import itertools

blosum_json_file_path = "../starter_code/blosum62.json"
organisms_json_file_path = "../starter_code/organisms.json"

with open(blosum_json_file_path, 'r') as j:
    blosum = json.loads(j.read())

with open(organisms_json_file_path, 'r') as j:
    organisms = json.loads(j.read())

def needleman_wunsch(seq1: str, seq2:str, switch_cost:dict):
    # algorithm adapted from https://bostjan-cigan.medium.com/using-the-needleman-wunsch-algorithm-to-draw-evolutionary-trees-90d9db149413
    m = len(seq1)+1 
    n = len(seq2)+1 
 
    M = np.zeros((m, n))

    M[0][0] = 0
    for i in range(1, m):
        M[i][0] = M[i-1][0] + switch_cost[seq1[i-1]]
    for j in range(1, n):
        M[0][j] = M[0][j-1] + switch_cost[seq2[j-1]]

    for i in range(1, m):
        for j in range(1, n):
            match = M[i-1][j-1] + switch_cost[seq1[i-1]+seq2[j-1]]
            delete1 = M[i-1][j]+ switch_cost[seq1[i-1]]
            delete2 = M[i][j-1]+ switch_cost[seq2[j-1]]

            M[i][j] = max(match, delete1, delete2)
 
    return M[-1][-1]

all_animals = list(organisms.keys())
all_pairs = itertools.combinations(all_animals, 2)

all_scores = {}
for pair in all_pairs:
    seq1 = organisms.get(pair[0])
    seq2 = organisms.get(pair[1])
    NW = needleman_wunsch(seq1, seq2, blosum)
    all_scores[pair[0]+"_"+pair[1]] = int(NW)

with open("./organisms_scores_blosum62.json", 'w') as j:
    json.dump(all_scores, j)
