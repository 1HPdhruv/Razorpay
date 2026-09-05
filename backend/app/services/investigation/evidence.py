import pandas as pd
from typing import List, Dict
import uuid
from app.services.investigation.evidence_pack import EvidencePack, EvidenceItem
from app.models.pattern import Pattern

def _apply_conditions(df: pd.DataFrame, conditions: List[Dict]) -> pd.Series:
    mask = pd.Series([True]*len(df), index=df.index)
    for cond in conditions:
        f = cond.feature
        v = cond.value
        op = cond.operator
        if op == '==':
            mask &= (df[f] == v)
    return mask

def retrieve_evidence(pattern: Pattern, feat_df: pd.DataFrame, ev_df: pd.DataFrame) -> EvidencePack:
    # Build mask for pattern matches
    mask = _apply_conditions(feat_df, pattern.conditions)
    
    matched_df = feat_df[mask]
    baseline_df = feat_df[~mask]
    
    loss_matches = matched_df[matched_df['loss_flag'] == True]
    non_loss_matches = matched_df[matched_df['loss_flag'] == False]
    
    supporting_loss = loss_matches.head(5).to_dict(orient='records')
    contrasting_non_loss = non_loss_matches.head(3).to_dict(orient='records')
    baseline_examples = baseline_df.head(3).to_dict(orient='records')
    
    evidence_items = []
    
    # Generate abstract evidence items
    ev_id_idx = 1
    
    for ex in supporting_loss:
        tx_id = ex['transaction_id']
        evidence_items.append(EvidenceItem(
            evidence_id=f"EV-{ev_id_idx:03d}",
            transaction_id=tx_id,
            evidence_type="LOSS_OUTCOME",
            claim="Transaction matched pattern and resulted in loss.",
            observed_value=str(ex['loss_amount']),
            source_field="loss_amount"
        ))
        ev_id_idx += 1
        
    for ex in contrasting_non_loss:
        tx_id = ex['transaction_id']
        evidence_items.append(EvidenceItem(
            evidence_id=f"EV-{ev_id_idx:03d}",
            transaction_id=tx_id,
            evidence_type="COMPARISON",
            claim="Transaction matched pattern but did NOT result in loss.",
            observed_value="0",
            source_field="loss_amount"
        ))
        ev_id_idx += 1

    return EvidencePack(
        pattern=pattern,
        pattern_statistics={
            "support": pattern.support,
            "loss_rate": pattern.loss_rate,
            "baseline_loss_rate": pattern.baseline_loss_rate,
            "lift": pattern.lift
        },
        supporting_loss_examples=supporting_loss,
        contrasting_non_loss_examples=contrasting_non_loss,
        baseline_examples=baseline_examples,
        evidence_items=evidence_items
    )
