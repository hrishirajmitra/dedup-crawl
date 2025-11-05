# --- File: pipeline/classification.py ---

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates using a "normalized sum."
    
    This calculation ignores missing fields (NaNs) instead of
    treating them as a 0.0 penalty, making it much more
    robust to incomplete data.
    """
    
    # 1. Sum the scores for available (non-NaN) fields
    sum_scores = features.sum(axis=1)
    
    # 2. Count how many fields were available (non-NaN)
    count_scores = features.notna().sum(axis=1)
    
    # 3. Get the total number of fields we are comparing
    num_total_fields = len(features.columns)
    
    # 4. Calculate the normalized sum
    # (Sum / Count) * Total = Scaled Score
    # We use .fillna(0) to handle division by zero if a row has 0 valid fields
    normalized_sum = (sum_scores / count_scores).fillna(0) * num_total_fields
    
    # 5. Classify using the same threshold as before
    matches = features[normalized_sum >= threshold]
    
    # Return the MultiIndex of matching pairs
    return matches.index