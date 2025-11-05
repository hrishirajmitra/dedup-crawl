# --- File: pipeline/comparison.py ---

import recordlinkage
from . import constants as const

def compare_pairs(candidate_pairs, df, comparison_fields):
    """
    Computes similarity features for each candidate pair.
    
    This version can handle both:
    - Single-field comparisons (e.g., given_name vs. given_name)
    - Crossed-field comparisons (e.g., given_name vs. surname)
    """
    compare_cl = recordlinkage.Compare()

    for comp in comparison_fields:
        method = comp[const.KEY_METHOD]
        label = comp[const.KEY_LABEL]
        
        # Determine field configuration
        if const.FIELD_SINGLE in comp:
            # Single field comparison (e.g., given_name vs given_name)
            field_left = comp[const.FIELD_SINGLE]
            field_right = comp[const.FIELD_SINGLE]
        elif const.FIELD_LEFT in comp and const.FIELD_RIGHT in comp:
            # Crossed fields comparison (e.g., given_name vs surname)
            field_left = comp[const.FIELD_LEFT]
            field_right = comp[const.FIELD_RIGHT]
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

        # Add comparison logic based on method
        if method == const.METHOD_STRING:
            algo = comp.get(const.KEY_STRING_METHOD, const.DEFAULT_STRING_ALGO)
            compare_cl.string(
                field_left,
                field_right,
                method=algo,
                threshold=comp[const.KEY_THRESHOLD],
                label=label
            )
        elif method == const.METHOD_EXACT:
            compare_cl.exact(
                field_left,
                field_right,
                label=label
            )
    
    # Compute the features for all pairs
    features = compare_cl.compute(candidate_pairs, df)
    
    return features