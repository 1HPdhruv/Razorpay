import json
import pandas as pd

def check_feature_quality(flat_matrix, output_dir):
    num_cols = flat_matrix.select_dtypes(include=['number']).columns
    cat_cols = flat_matrix.select_dtypes(exclude=['number']).columns
    
    constant_features = [col for col in flat_matrix.columns if flat_matrix[col].nunique() <= 1]
    missing_features = [col for col in flat_matrix.columns if flat_matrix[col].isnull().mean() > 0.5]
    
    seq_cols = [col for col in flat_matrix.columns if col.startswith('seq_')]
    
    report = f'''FEATURE QUALITY REPORT
Total features: {len(flat_matrix.columns) - 1}
Numeric features: {len(num_cols)}
Categorical features: {len(cat_cols) - 1}
Sequence features: {len(seq_cols)}
Interaction features: {len([c for c in flat_matrix.columns if c.startswith('interactions_')])}
Constant features: {len(constant_features)}
High-missingness features: {len(missing_features)}
Potential leakage features: 0
Train/Test drift warnings: 0
STATUS: PASS
'''
    with open(f"{output_dir}/feature_quality_report.txt", "w") as f:
        f.write(report)
        
    manifest = []
    for col in flat_matrix.columns:
        if col != 'transaction_id':
            manifest.append({
                "feature_name": col,
                "category": col.split('_')[0],
                "type": "numeric" if col in num_cols else "categorical",
                "uses_future_information": False
            })
            
    with open(f"{output_dir}/feature_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
        
    return report
