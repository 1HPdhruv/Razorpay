import pandas as pd
import scipy.stats as stats
from itertools import combinations
from app.core.constants import DISCOVERY_CONFIG

def compute_fisher_exact(pattern_matches, non_pattern_matches, pattern_losses, non_pattern_losses):
    pattern_non_losses = pattern_matches - pattern_losses
    non_pattern_non_losses = non_pattern_matches - non_pattern_losses
    
    table = [
        [pattern_losses, pattern_non_losses],
        [non_pattern_losses, non_pattern_non_losses]
    ]
    
    _, p_value = stats.fisher_exact(table, alternative='greater')
    return p_value

def mine_associations(df, target_df):
    data = pd.merge(df, target_df[['transaction_id', 'loss_flag', 'loss_amount']], on='transaction_id')
    total_tx = len(data)
    total_losses = data['loss_flag'].sum()
    baseline_loss_rate = total_losses / total_tx if total_tx > 0 else 0
    
    min_support = DISCOVERY_CONFIG['MIN_SUPPORT']
    min_lift = DISCOVERY_CONFIG['MIN_LIFT']
    
    exclude_cols = ['transaction_id', 'loss_flag', 'loss_amount', 'financial_amount_paise']
    cat_cols = [c for c in data.columns if c not in exclude_cols and not c.startswith('seq_') and not c.startswith('interactions_')]
    
    itemsets = {}
    for col in cat_cols:
        for val in data[col].unique():
            if pd.isna(val): continue
            mask = data[col] == val
            support = mask.mean()
            if support >= min_support:
                itemsets[f"{col}=={val}"] = mask

    candidates = []
    items = list(itemsets.keys())
    
    # Single items
    for item in items:
        mask = itemsets[item]
        losses = data.loc[mask, 'loss_flag'].sum()
        if losses < DISCOVERY_CONFIG['MIN_LOSS_COUNT']: continue
        
        matches = mask.sum()
        loss_rate = losses / matches
        if loss_rate <= baseline_loss_rate: continue
        
        lift = loss_rate / baseline_loss_rate if baseline_loss_rate > 0 else 0
        if lift < min_lift: continue
        
        non_matches = total_tx - matches
        non_losses = total_losses - losses
        p_val = compute_fisher_exact(matches, non_matches, losses, non_losses)
        
        if p_val <= DISCOVERY_CONFIG['P_VALUE_THRESHOLD']:
            candidates.append({
                'conditions': [item],
                'mask': mask,
                'support': matches / total_tx,
                'matches': matches,
                'losses': losses,
                'loss_rate': loss_rate,
                'lift': lift,
                'p_value': p_val,
                'exposure': data.loc[mask, 'loss_amount'].sum()
            })
            
    # Pairs (Size 2 interactions)
    valid_items = [i for i in items if data.loc[itemsets[i], 'loss_flag'].sum() > 0]
    pairs = []
    for i, j in combinations(valid_items, 2):
        if i.split('==')[0] == j.split('==')[0]: continue
        
        mask = itemsets[i] & itemsets[j]
        matches = mask.sum()
        if matches / total_tx < min_support: continue
        
        losses = data.loc[mask, 'loss_flag'].sum()
        if losses < DISCOVERY_CONFIG['MIN_LOSS_COUNT']: continue
        
        loss_rate = losses / matches
        lift = loss_rate / baseline_loss_rate if baseline_loss_rate > 0 else 0
        if lift < min_lift: continue
        
        non_matches = total_tx - matches
        non_losses = total_losses - losses
        p_val = compute_fisher_exact(matches, non_matches, losses, non_losses)
        
        if p_val <= DISCOVERY_CONFIG['P_VALUE_THRESHOLD']:
            pairs.append({
                'conditions': [i, j],
                'mask': mask,
                'support': matches / total_tx,
                'matches': matches,
                'losses': losses,
                'loss_rate': loss_rate,
                'lift': lift,
                'p_value': p_val,
                'exposure': data.loc[mask, 'loss_amount'].sum()
            })
            
    candidates.extend(pairs)
    
    # Triplets
    for p in pairs:
        for item in valid_items:
            if item in p['conditions']: continue
            if item.split('==')[0] in [c.split('==')[0] for c in p['conditions']]: continue
            
            mask = p['mask'] & itemsets[item]
            matches = mask.sum()
            if matches / total_tx < min_support: continue
            
            losses = data.loc[mask, 'loss_flag'].sum()
            if losses < DISCOVERY_CONFIG['MIN_LOSS_COUNT']: continue
            
            loss_rate = losses / matches
            lift = loss_rate / baseline_loss_rate if baseline_loss_rate > 0 else 0
            if lift < min_lift: continue
            
            non_matches = total_tx - matches
            non_losses = total_losses - losses
            p_val = compute_fisher_exact(matches, non_matches, losses, non_losses)
            
            if p_val <= DISCOVERY_CONFIG['P_VALUE_THRESHOLD']:
                candidates.append({
                    'conditions': sorted(p['conditions'] + [item]),
                    'mask': mask,
                    'support': matches / total_tx,
                    'matches': matches,
                    'losses': losses,
                    'loss_rate': loss_rate,
                    'lift': lift,
                    'p_value': p_val,
                    'exposure': data.loc[mask, 'loss_amount'].sum()
                })
                
    unique_cands = {}
    for c in candidates:
        key = tuple(sorted(c['conditions']))
        if key not in unique_cands:
            unique_cands[key] = c
            
    return list(unique_cands.values()), baseline_loss_rate, data
