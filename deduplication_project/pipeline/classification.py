# --- File: pipeline/classification.py ---

import pandas as pd
import numpy as np
import config

def _get_normalized_score(features, fields, weights):
    """
    Helper function to calculate a weighted, normalized score
    for a specific set of fields.
    """
    # Filter to fields that actually exist in the features
    existing_fields = [f for f in fields if f in features.columns]
    if not existing_fields:
        return 0
        
    sub_features = features[existing_fields]
    sub_weights = weights[existing_fields]
    
    # Calculate weighted scores
    weighted_scores = sub_features * sub_weights
    
    # Sum the weighted scores for available (non-NaN) fields
    sum_scores = weighted_scores.sum(axis=1)
    
    # Sum the *weights* of the available (non-NaN) fields
    available_weights_features = sub_features.notna() * sub_weights
    count_scores = available_weights_features.sum(axis=1)
    
    # Get the total possible weight for this group of fields
    num_total_fields = sub_weights.sum()
    
    # Calculate the normalized sum (score 0-N)
    normalized_sum = (sum_scores / count_scores).fillna(0) * num_total_fields
    
    return normalized_sum

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates using hybrid logic:
    1. 'name_score' is a SIMPLE SUM (acts as a gate).
    2. 'address_score' and 'detail_score' are NORMALIZED & WEIGHTED.
    """
    
    # 1. Get the weights from config
    weights = {
        comp['label']: comp.get('weight', 1.0) 
        for comp in config.COMPARISON_FIELDS
    }
    weights = pd.Series(weights)

    # --- 1. Calculate the 'name_score' (Simple Sum) ---
    # This is our 'gate' - must have *some* name similarity
    score_gg = features.get('given_name', 0).fillna(0) * weights.get('given_name', 1)
    score_ss = features.get('surname', 0).fillna(0) * weights.get('surname', 1)
    name_match_score = score_gg + score_ss
    
    score_gvsn = features.get('gv_vs_sn', 0).fillna(0) * weights.get('gv_vs_sn', 1)
    score_sngv = features.get('sn_vs_gv', 0).fillna(0) * weights.get('sn_vs_gv', 1)
    cross_match_score = score_gvsn + score_sngv
    
    # Get the best possible name score
    final_name_score = name_match_score.combine(cross_match_score, max)
    
    # --- 2. Calculate the 'address_score' (Normalized & Weighted) ---
    address_fields = [
        'street_number', 'address_1', 'address_2',
        'suburb', 'postcode', 'state'
    ]
    address_score = _get_normalized_score(features, address_fields, weights)

    # --- 3. Calculate the 'detail_score' (Normalized & Weighted) ---
    detail_fields = ['date_of_birth', 'soc_sec_id']
    detail_score = _get_normalized_score(features, detail_fields, weights)
    
    # --- 4. Calculate total score ---
    # Total = (Best Name) + (Norm. Address) + (Norm. Details)
    total_score = final_name_score + address_score + detail_score
    
    # --- 5. Classify ---
    matches = total_score >= threshold
    return total_score[matches]