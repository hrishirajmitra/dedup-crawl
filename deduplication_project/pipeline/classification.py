# --- File: pipeline/classification.py ---

import pandas as pd

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates using advanced logic.
    
    It checks for both (A->A, B->B) and (A->B, B->A) name matches
    and combines that with the score from other fields.
    """
    
    # --- 1. Calculate the 'address' score (all fields *except* names) ---
    address_fields = ['address_1', 'suburb', 'state']
    
    # Filter 'features' to only include address fields that actually exist
    existing_address_fields = [f for f in address_fields if f in features.columns]
    address_score = features[existing_address_fields].sum(axis=1)

    # --- 2. Calculate the 'name' scores ---
    
    # Score for a normal match (given_name->given_name, surname->surname)
    # Check if columns exist, default to 0 if not
    score_gg = features.get('given_name', 0)
    score_ss = features.get('surname', 0)
    name_match_score = score_gg + score_ss
    
    # Score for a crossed match (given_name->surname, surname->given_name)
    score_gvsn = features.get('gv_vs_sn', 0)
    score_sngv = features.get('sn_vs_gv', 0)
    cross_match_score = score_gvsn + score_sngv
    
    # --- 3. Find the *best* name score ---
    # For each pair, take the HIGHEST of the two scores
    final_name_score = name_match_score.combine(cross_match_score, max)
    
    # --- 4. Calculate total score ---
    # Total = (Best Name Score) + (Address Score)
    total_score = final_name_score + address_score
    
    # --- 5. Classify ---
    # Compare against the config threshold
    matches = features[total_score >= threshold]
    
    # Return the MultiIndex of matching pairs
    return matches.index