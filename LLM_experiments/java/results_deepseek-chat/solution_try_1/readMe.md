# Phylogenetic Analysis Tool

## Description
Java-based pipeline for:
1. Sequence alignment (Needleman-Wunsch)
2. Phylogenetic tree construction
3. Threshold-based clustering

## Input Files
Place these in `src/main/resources/`:
- `organisms.json`: Species → sequences mapping
- `blosumXX.json`: BLOSUM matrices
- `thresholds.txt`: One threshold per line

## Output Files
Generated in project root:
- `*_scores_*.json`: Alignment scores
- `tree_*.nw`: Newick formats
- `phylogenetic_tree_*.png`: Dendrogram
- `clusters_*.json`: Threshold-based clusters

## Build & Run
```bash
mvn clean package
java -jar target/phylo-project-1.0-SNAPSHOT.jar
```

## Dependencies
- Java 21
- Maven 3.9+
```

---

### **2. Input Files (Place in `src/main/resources/`)**

#### **blosum50.json** (Example BLOSUM Matrix)
```json
{"A":4,"R":-1,"N":-2,"D":-2,"C":0,"AA":5,"AR":-1,"AN":-2,"AD":-2,"AC":-1,...}
```
**Description**: Substitution scores for BLOSUM50.

---

#### **organisms.json** (Example Species Data)
```json
{
  "Human": "MTHQTHAYHMVNPSPWPLTGALSALLMTSGL",
  "Chimpanzee": "MTHQTHAYHMVNPSPWPLTGALSALLMTS",
  "Mouse": "MTHQTHAYHMVNPSPWPLTGALSALLMT"
}
```
**Description**: Species and their amino acid sequences.

---

#### **thresholds.txt**
```text
1200
800
500
```
**Description**: Similarity thresholds for clustering.

---

### **3. Generated Output Files**
These will be created automatically in the project root:
1. `organisms_scores_blosum50.json`  
2. `tree_blosum50_newick.nw`  
3. `tree_blosum50_newick_with_distance.nw`  
4. `phylogenetic_tree_blosum50.png`  
5. `clusters_for_blosum50.json`  

---