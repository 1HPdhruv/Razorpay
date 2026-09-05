from app.services.discovery.association import mine_associations
from app.models.pattern import Pattern, PatternCondition
import pandas as pd
import math
import uuid

class PatternDiscoveryEngine:
    def __init__(self):
        self.known_rules = [] # We'll populate this with R1-R4 signatures if needed
        
    def discover(self, train_features: pd.DataFrame, train_targets: pd.DataFrame):
        candidates, baseline_rate, merged_data = mine_associations(train_features, train_targets)
        
        # Deduplicate
        # If a subset exists with very similar loss stats, keep the more general one or the one with higher lift
        # For simplicity, we just rank them and filter overlapping masks.
        
        # Score candidates
        # Score = log2(matches) * lift * (1 - p_value)
        scored = []
        for c in candidates:
            score = math.log2(c['matches'] + 1) * c['lift'] * (1 - c['p_value'])
            c['score'] = score
            scored.append(c)
            
        scored = sorted(scored, key=lambda x: x['score'], reverse=True)
        
        # Greedy deduplication based on transaction overlap
        final_candidates = []
        seen_masks = []
        
        for c in scored:
            overlap = False
            for sm in seen_masks:
                # If jaccard similarity of matches > 0.8, consider duplicate
                intersection = (c['mask'] & sm).sum()
                union = (c['mask'] | sm).sum()
                if intersection / union > 0.8:
                    overlap = True
                    break
            
            if not overlap:
                final_candidates.append(c)
                seen_masks.append(c['mask'])
                if len(final_candidates) >= 50:
                    break
                    
        # Format output
        patterns = []
        for idx, c in enumerate(final_candidates):
            conds = []
            desc_parts = []
            for cond_str in c['conditions']:
                f, v = cond_str.split('==')
                conds.append(PatternCondition(feature=f, operator='==', value=v))
                desc_parts.append(f"{f.replace('atomic_', '').replace('temporal_', '').replace('behavioral_', '')} is {v}")
                
            evidence_tx = merged_data[c['mask']]['transaction_id'].tolist()[:50]
            
            p = Pattern(
                pattern_id=f"PTN_{idx+1}",
                name=f"Pattern {idx+1}",
                description=f"Transactions where {' and '.join(desc_parts)} show a substantially elevated loss rate.",
                pattern_type="ASSOCIATION",
                conditions=conds,
                support=c['support'],
                matching_transaction_count=c['matches'],
                loss_count=c['losses'],
                loss_rate=c['loss_rate'],
                baseline_loss_rate=baseline_rate,
                risk_multiplier=c['lift'],
                lift=c['lift'],
                p_value=c['p_value'],
                exposure_amount=c['exposure'],
                average_loss_amount=c['exposure']/c['losses'] if c['losses'] > 0 else 0,
                discovery_method="Association Mining + Fisher's Exact Test",
                feature_importance={},
                evidence_transaction_ids=evidence_tx,
                status="EMERGENT"
            )
            patterns.append(p)
            
        return patterns
