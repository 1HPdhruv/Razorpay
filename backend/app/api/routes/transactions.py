from fastapi import APIRouter, HTTPException
import pandas as pd
import os

router = APIRouter()

from app.core.config import settings

def _load_transactions():
    path = settings.DATA_DIR / "train" / "transactions.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path)
    df = df.where(pd.notnull(df), None)
    # Take first 50 for preview
    return df.head(50).to_dict(orient='records')

@router.get("")
def list_transactions():
    return _load_transactions()

@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    path = settings.DATA_DIR / "train" / "transactions.csv"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Dataset not found")
    df = pd.read_csv(path)
    df = df.where(pd.notnull(df), None)
    tx = df[df['transaction_id'] == transaction_id]
    if tx.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx.iloc[0].to_dict()

@router.get("/{transaction_id}/dna")
def get_transaction_dna(transaction_id: str):
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))
    from app.services.features.extractor import extract_features
    
    tx_path = settings.DATA_DIR / "train" / "transactions.csv"
    ev_path = settings.DATA_DIR / "train" / "events.csv"
    
    if not tx_path.exists() or not ev_path.exists():
        raise HTTPException(status_code=404, detail="Data not generated")
        
    tx_df = pd.read_csv(tx_path)
    ev_df = pd.read_csv(ev_path)
    
    tx = tx_df[tx_df['transaction_id'] == transaction_id]
    if tx.empty:
        raise HTTPException(status_code=404, detail="Transaction not found")
        
    ev = ev_df[ev_df['transaction_id'] == transaction_id]
    dna_list = extract_features(tx, ev)
    
    if not dna_list:
        raise HTTPException(status_code=500, detail="Failed to extract DNA")
        
    return dna_list[0]

