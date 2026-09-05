import pytest
from app.services.data.generator import generate_synthetic_data
import os
import shutil

def test_reproducibility():
    os.makedirs("data/test_gen1", exist_ok=True)
    os.makedirs("data/test_gen2", exist_ok=True)

    tx1, ev1 = generate_synthetic_data(100, 42, "data/test_gen1")
    tx2, ev2 = generate_synthetic_data(100, 42, "data/test_gen2")

    assert len(tx1) == len(tx2)
    assert tx1.iloc[0]['transaction_id'] == tx2.iloc[0]['transaction_id']

    shutil.rmtree("data/test_gen1")
    shutil.rmtree("data/test_gen2")
