# --- File: pipeline/comparison.py ---

import recordlinkage

def compare_pairs(candidate_pairs, df, comparison_fields):
    """
    Computes similarity features for each candidate pair.
    
    This version can handle both:
    - Single-field comparisons (e.g., given_name vs. given_name)
    - Crossed-field comparisons (e.g., given_name vs. surname)
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
            print(f"Warning: Skipping comparison '{label}' - incorrect field config.")
            continue
            
        # Validate columns exist
        if field_left not in df.columns:
            print(f"Warning: Field '{field_left}' not in DataFrame. Skipping '{label}'.")
            continue
        if field_right not in df.columns:
            print(f"Warning: Field '{field_right}' not in DataFrame. Skipping '{label}'.")
            continue

        # --- Add comparison logic ---
        if method == "string":
            algo = comp.get("string_method", "jarowinkler")
            compare_cl.string(field_left, field_right, 
                              method=algo, 
                              threshold=comp["threshold"], 
                              label=label)
        elif method == "exact":
            compare_cl.exact(field_left, field_right, 
                             label=label)
        
    # Compute the features for all pairs
    features = compare_cl.compute(candidate_pairs, df)
    
    return features