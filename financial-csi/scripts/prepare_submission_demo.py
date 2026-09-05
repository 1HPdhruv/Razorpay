#!/usr/bin/env python3
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

if __name__ == "__main__":
    print("Executing Canonical Submission Demo Preparation...")
    # This directly triggers the verified demo preparation script
    run("python scripts/prepare_demo.py")
    print("Demo artifacts safely regenerated.")
