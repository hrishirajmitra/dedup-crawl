# --- File: pipeline/comparison.py ---

import recordlinkage

def compare_pairs(candidate_pairs, df, comparison_fields):
    """
    Computes similarity features for each candidate pair.
    
    It iterates through the fields defined in the config and
    applies the specified comparison method (string, exact, etc.).
    """
    compare_cl = recordlinkage.Compare()

    for comp in comparison_fields:
        field = comp["field"]
        method = comp["method"]
        
        if field not in df.columns:
            print(f"Warning: Comparison field '{field}' not in DataFrame. Skipping.")
            continue

        if method == "string":
            # Read the string_method from config, default to 'jarowinkler'
            algo = comp.get("string_method", "jarowinkler")
            
            compare_cl.string(field, field, 
                              method=algo, 
                              threshold=comp["threshold"], 
                              label=field)
        elif method == "exact":
            compare_cl.exact(field, field, 
                             label=field)
        # Add other methods like 'numeric' if needed
        
    # Compute the features for all pairs
    features = compare_cl.compute(candidate_pairs, df)
    
    return features