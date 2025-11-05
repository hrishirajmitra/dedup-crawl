# --- File: pipeline/classification.py ---

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates using a "normalized sum."
    
    (MODIFIED) Returns a Series of pairs that passed the
    threshold, with their corresponding scores.
    """
    
    # 1. Sum the scores for available (non-NaN) fields
    sum_scores = features.sum(axis=1)
    
    # 2. Count how many fields were available (non-NaN)
    count_scores = features.notna().sum(axis=1)
    
    # 3. Get the total number of fields we are comparing
    num_total_fields = len(features.columns)
    
    # 4. Calculate the normalized sum
    normalized_sum = (sum_scores / count_scores).fillna(0) * num_total_fields
    
    # 5. Classify using the threshold
    matches = normalized_sum >= threshold
    
    # 6. (MODIFIED) Return the Series of passing scores
    # This Series has the (pair) as the index and (score) as the value
    return normalized_sum[matches]