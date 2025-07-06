# Phylogenetic Analysis Pipeline

## Overview
This pipeline performs:
1. Sequence alignment using Needleman-Wunsch
2. Phylogenetic tree construction
3. Threshold-based species clustering
4. Dendrogram visualization

## Requirements
- Python 3.11
- Pyenv (recommended)

## Setup
```bash
python -m venv phylo_env
source phylo_env/bin/activate  # Linux/Mac
phylo_env\Scripts\activate    # Windows
pip install -r requirements.txt
```

## Input Files
1. `organisms.json`: Species-to-sequence mapping
   ```json
   {"Species1": "MTHQTHAY...", "Species2": "MTHQTH..."}
   ```
2. `blosumXX.json`: BLOSUM matrix (XX = 50 or 62)
3. `thresholds.txt`: One integer per line

## Execution
```bash
python main.py blosum62.json
```

## Output Files
| File | Description |
|------|-------------|
| `organisms_scores_blosumXX.json` | Pairwise similarity scores |
| `tree_blosumXX_newick.nw` | Basic Newick tree |
| `tree_blosumXX_newick_with_distance.nw` | Newick with distances |
| `phylogenetic_tree_blosumXX.png` | Dendrogram visualization |
| `clusters_for_blosumXX.json` | Threshold-based clusters |

## Example Output
```
Threshold: 1200
Clusters: 2
  Cluster 1: SpeciesA, SpeciesB
  Cluster 2: SpeciesC, SpeciesD, SpeciesE
```
```

---

### 3. Sample Input Files (Place in Project Root)  

#### `organisms.json` (Example)  
```json
{
  "Wild boar": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
  "Horse": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
}
```

#### `blosum62.json` (Example)  
```json
{
  "A": 4, "R": -1, "N": -2, "D": -2, "C": 0,
  "AR": -1, "AN": -2, "AD": -2, "AC": -3,
  "AA": 4, "RR": 5, "NN": 6, "DD": 6, "CC": 9
}
```

#### `thresholds.txt` (Example)  
```
1200
1350
1500
```