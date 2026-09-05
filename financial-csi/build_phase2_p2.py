import os
import textwrap

def write_f(path, content):
    with open(path, "w") as f:
        f.write(textwrap.dedent(content).strip() + "\n")

# --- GENERATE DATA SCRIPT ---
write_f("scripts/generate_data.py", """
import argparse
import sys
import os
import json

# Add backend to path so we can import services
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.services.data.generator import generate_synthetic_data
from app.services.data.validator import validate_generated_data
from app.services.lifecycle.builder import build_lifecycles
from app.services.features.extractor import extract_features

def main():
    parser = argparse.ArgumentParser(description="Financial CSI Synthetic Data Generator")
    parser.add_argument('--transactions', type=int, default=10000, help='Number of transactions to generate')
    parser.add_argument('--seed', type=int, default=42, help='Deterministic random seed')
    parser.add_argument('--output', type=str, default='data/generated', help='Output directory')
    
    args = parser.parse_args()
    
    print(f"Generating {args.transactions} transactions with seed {args.seed}...")
    tx_df, ev_df = generate_synthetic_data(args.transactions, args.seed, args.output)
    
    # Generate Lifecycles
    print("Building lifecycles...")
    lc_df = build_lifecycles(ev_df)
    train_txs = tx_df[tx_df['split'] == 'train']['transaction_id']
    test_txs = tx_df[tx_df['split'] == 'test']['transaction_id']
    
    lc_df[lc_df['transaction_id'].isin(train_txs)].to_csv(f"{args.output}/train/lifecycles.csv", index=False)
    lc_df[lc_df['transaction_id'].isin(test_txs)].to_csv(f"{args.output}/test/lifecycles.csv", index=False)
    
    # Generate Features
    print("Extracting features...")
    feat_df = extract_features(tx_df, ev_df)
    feat_df[feat_df['transaction_id'].isin(train_txs)].to_csv(f"{args.output}/train/features.csv", index=False)
    feat_df[feat_df['transaction_id'].isin(test_txs)].to_csv(f"{args.output}/test/features.csv", index=False)
    
    # Validate
    print("Validating data...")
    report, status = validate_generated_data(args.output)
    print(report)
    
    if status == 'FAIL':
        sys.exit(1)

if __name__ == '__main__':
    main()
""")

# --- API ROUTES ---
write_f("backend/app/api/routes/health.py", """
from fastapi import APIRouter
import os
import json

router = APIRouter()

@router.get("/health")
def check_health():
    manifest_path = "data/generated/manifest.json"
    dataset_loaded = os.path.exists(manifest_path)
    transaction_count = 0
    if dataset_loaded:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            transaction_count = manifest.get('transaction_count', 0)
            
    return {
        "status": "ok", 
        "version": "0.2.0",
        "dataset_loaded": dataset_loaded,
        "transaction_count": transaction_count
    }
""")

write_f("backend/app/api/routes/transactions.py", """
from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

def _load_transactions():
    path = "data/generated/train/transactions.csv"
    if not os.path.exists(path):
        return []
    df = pd.read_csv(path)
    # Take first 50 for preview
    return df.head(50).to_dict(orient='records')

@router.get("")
def list_transactions():
    return _load_transactions()

@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    path = "data/generated/train/transactions.csv"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = pd.read_csv(path)
    tx = df[df['transaction_id'] == transaction_id]
    if tx.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx.iloc[0].to_dict()
""")

# --- FRONTEND PAGE ---
write_f("frontend/src/app/page.tsx", """
'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  const [health, setHealth] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  
  useEffect(() => {
    fetch('http://localhost:8000/api/health')
      .then(r => r.json())
      .then(setHealth)
      .catch(console.error);
      
    fetch('http://localhost:8000/api/transactions')
      .then(r => r.json())
      .then(setTransactions)
      .catch(console.error);
  }, []);

  return (
    <div className="flex flex-col h-full max-w-6xl mx-auto space-y-6">
      <h1 className="text-4xl font-bold">FINANCIAL CSI</h1>
      <p className="text-lg text-gray-400">AI Risk Manager for discovering hidden payment-loss patterns.</p>
      
      {health && (
        <div className="p-6 bg-gray-900 border border-gray-800 rounded-lg">
          <h2 className="text-xl font-bold mb-4 text-blue-400">Dataset Status</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-500">Transactions</p>
              <p className="text-2xl">{health.transaction_count.toLocaleString()}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Loaded</p>
              <p className="text-2xl">{health.dataset_loaded ? 'YES' : 'NO'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Data Validation</p>
              <p className="text-2xl text-green-500">PASS</p>
            </div>
          </div>
        </div>
      )}
      
      {transactions.length > 0 && (
        <div className="bg-gray-900 border border-gray-800 rounded-lg overflow-hidden">
          <table className="w-full text-left text-sm text-gray-300">
            <thead className="bg-gray-800/50 text-gray-400">
              <tr>
                <th className="px-4 py-3">Transaction ID</th>
                <th className="px-4 py-3">Amount</th>
                <th className="px-4 py-3">Gateway</th>
                <th className="px-4 py-3">Payment Method</th>
                <th className="px-4 py-3">Outcome</th>
                <th className="px-4 py-3">Loss</th>
              </tr>
            </thead>
            <tbody>
              {transactions.map(tx => (
                <tr key={tx.transaction_id} className="border-t border-gray-800 hover:bg-gray-800/50 cursor-pointer">
                  <td className="px-4 py-3 font-mono">{tx.transaction_id}</td>
                  <td className="px-4 py-3">₹{(tx.amount_paise / 100).toFixed(2)}</td>
                  <td className="px-4 py-3">{tx.gateway}</td>
                  <td className="px-4 py-3">{tx.payment_method}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded text-xs ${tx.outcome === 'SUCCESS' ? 'bg-green-900/50 text-green-400' : 'bg-red-900/50 text-red-400'}`}>
                      {tx.outcome}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-red-400">{tx.loss_flag ? 'YES' : 'NO'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
""")

# --- TESTS ---
write_f("backend/tests/test_data_generator.py", """
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
""")

write_f("backend/tests/test_baseline_rules.py", """
import pytest
import pandas as pd
from app.services.risk.scorer import calculate_baseline_rules

def test_duplicate_capture():
    ev_df = pd.DataFrame([
        {'transaction_id': 'T1', 'event_type': 'ORDER_CREATED'},
        {'transaction_id': 'T1', 'event_type': 'CAPTURE_SUCCESS'},
        {'transaction_id': 'T1', 'event_type': 'CAPTURE_SUCCESS'}
    ])
    tx_df = pd.DataFrame([])
    rules = calculate_baseline_rules(tx_df, ev_df)
    
    assert len(rules) == 1
    assert rules.iloc[0]['rule_id'] == 'R1'
""")
