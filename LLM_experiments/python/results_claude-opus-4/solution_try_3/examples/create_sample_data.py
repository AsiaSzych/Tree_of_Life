"""Create sample data files for testing the phylogenetic analysis pipeline."""

import json
import random
from pathlib import Path


def create_sample_organisms(num_species: int = 5, seq_length: int = 30):
    """Create sample organism data."""
    amino_acids = "ACDEFGHIKLMNPQRSTVWY"
    organisms = {}
    
    # Create a base sequence
    base_seq = ''.join(random.choices(amino_acids, k=seq_length))
    
    for i in range(num_species):
        # Create variations of the base sequence
        seq = list(base_seq)
        # Introduce random mutations
        num_mutations = random.randint(1, seq_length // 5)
        for _ in range(num_mutations):
            pos = random.randint(0, seq_length - 1)
            seq[pos] = random.choice(amino_acids)
        
        organisms[f"Species_{i+1}"] = ''.join(seq)
    
    return organisms


def create_sample_blosum():
    """Create a simplified BLOSUM-like matrix."""
    amino_acids = "ACDEFGHIKLMNPQRSTVWY"
    blosum = {}
    
    # Gap penalties
    for aa in amino_acids:
        blosum[aa.lower()] = -2
    
    # Substitution scores
    for aa1 in amino_acids:
        for aa2 in amino_acids:
            key = f"{aa1.lower()}{aa2.lower()}"
            if aa1 == aa2:
                blosum[key] = 4  # Match
            else:
                blosum[key] = random.randint(-3, -1)  # Mismatch
    
    return blosum


def create_sample_thresholds():
    """Create sample threshold values."""
    # These will be adjusted based on actual score ranges
    return [50, 75, 100, 125, 150]


def main():
    """Generate all sample files."""
    output_dir = Path(".")
    
    # Create organisms.json
    organisms = create_sample_organisms(num_species=8)
    with open(output_dir / "organisms.json", "w") as f:
        json.dump(organisms, f, indent=2)
    print("Created organisms.json")
    
    # Create BLOSUM matrices
    blosum = create_sample_blosum()
    
    with open(output_dir / "blosum50.json", "w") as f:
        json.dump(blosum, f, indent=2)
    print("Created blosum50.json")
    
    with open(output_dir / "blosum62.json", "w") as f:
        json.dump(blosum, f, indent=2)
    print("Created blosum62.json")
    
    # Create thresholds.txt
    thresholds = create_sample_thresholds()
    with open(output_dir / "thresholds.txt", "w") as f:
        for t in thresholds:
            f.write(f"{t}\n")
    print("Created thresholds.txt")
    
    print("\nSample data files created successfully!")
    print("You can now run: python run_analysis.py")


if __name__ == "__main__":
    main()