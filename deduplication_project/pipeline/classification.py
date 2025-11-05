# --- File: pipeline/classification.py ---

import pandas as pd
# --- File: pipeline/classification.py ---

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates based on a simple sum threshold.
    
    The advanced logic is no longer needed because the
    swapped-name problem was solved in preprocessing.
    """
    # Sum the scores from all comparison fields
    total_score = features.sum(axis=1)
    
    # Select pairs that meet or exceed the threshold
    matches = features[total_score >= threshold]
    
    # Return the MultiIndex of matching pairs
    return matches.index