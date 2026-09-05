import os
import sys
from pathlib import Path
import subprocess

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def run(cmd):
    print(f"Running: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=PROJECT_ROOT)
    if res.returncode != 0:
        print(f"Failed: {cmd}")
        sys.exit(1)

def main():
    print("Preparing Financial CSI Demo Data...")
    
    # 1. Clear existing data
    run("rm -rf data/generated/*")
    
    # 2. Generate Deterministic Synthetic Data
    run("python scripts/generate_data.py --transactions 10000 --seed 42 --output data/generated")
    
    # 3. Discover Patterns
    run("python scripts/discover_patterns.py --train-features data/generated/train/feature_matrix.csv --train-targets data/generated/train/loss_targets.csv --output data/generated/discovered_patterns.json")
    
    # 4. Run Experiment / Simulations
    run("python scripts/run_simulation_experiment.py")
    
    # 5. Run Final Evaluation
    run("python scripts/run_final_evaluation.py")
    
    print("Demo preparation complete! You can now start the frontend and backend.")

if __name__ == "__main__":
    main()
