# --- File: pipeline/comparison.py ---

import recordlinkage
import numpy as np  # Required for np.nan

def compare_pairs(candidate_pairs, df, comparison_fields):
    """
    Computes similarity features for each candidate pair.
    
    - Handles both single and crossed-field comparisons.
    - Sets 'missing_value=np.nan' to ignore missing fields.
    """
    compare_cl = recordlinkage.Compare()

    for comp in comparison_fields:
        method = comp["method"]
        label = comp["label"]
        
        # Check for single field (e.g., given_name vs given_name)
        if "field" in comp:
            field_left = comp["field"]
            field_right = comp["field"]
        # Check for crossed fields (e.g., given_name vs surname)
        elif "field_left" in comp and "field_right" in comp:
            field_left = comp["field_left"]
            field_right = comp["field_right"]
        else:
            continue
            
        if field_left not in df.columns:
            continue
        if field_right not in df.columns:
            continue

        if method == "string":
            algo = comp.get("string_method", "jarowinkler")
            compare_cl.string(field_left, field_right, 
                              method=algo, 
                              threshold=comp["threshold"], 
                              label=label,
                              missing_value=np.nan)
        elif method == "exact":
            compare_cl.exact(field_left, field_right, 
                             label=label,
                             missing_value=np.nan)
        
    features = compare_cl.compute(candidate_pairs, df)
    
    return features