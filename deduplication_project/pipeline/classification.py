# --- File: pipeline/classification.py ---

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates based on a simple sum threshold.
    
    Adds up the similarity scores for each pair and checks if
    the total is >= the threshold.
    """
    # Sum the scores from all comparison fields
    total_score = features.sum(axis=1)
    
    # Select pairs that meet or exceed the threshold
    matches = features[total_score >= threshold]
    
    # Return the MultiIndex of matching pairs
    return matches.index