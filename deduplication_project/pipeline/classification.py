# --- File: pipeline/classification.py ---

import pandas as pd
import numpy as np  # <-- Make sure this is imported
import config

# --- (NEW) Outlier Trimming Configuration ---
# If a pair's average score is ABOVE this...
TRIM_AVG_THRESHOLD = 0.8
# ...and its minimum score is BELOW this...
TRIM_MIN_THRESHOLD = 0.1
# ...we will ignore the single lowest score.

def find_duplicates(features, threshold):
    """
    Classifies pairs as duplicates using a "Trimmed Weighted Normalized Sum."
    
    This is the most advanced classifier:
    1. It finds and "trims" (ignores) outlier low scores
       on otherwise high-matching pairs.
    2. It then calculates the "Weighted Normalized Sum" on
       the remaining (non-NaN) fields.
    """
    
    # --- 1. (NEW) Outlier Trimming Logic ---
    
    # Calculate the unweighted mean and min for all pairs
    unweighted_mean = features.mean(axis=1)
    unweighted_min = features.min(axis=1)
    
    # Find the pairs that meet our outlier condition
    outlier_mask = (unweighted_mean > TRIM_AVG_THRESHOLD) & \
                   (unweighted_min < TRIM_MIN_THRESHOLD)
    
    if outlier_mask.any():
        print(f"Trimming outliers from {outlier_mask.sum()} pairs...")
        
        # Get the field name (label) of the lowest score for each outlier row
        outlier_field_labels = features[outlier_mask].idxmin(axis=1)
        
        # Convert those specific [row, col] locations to np.nan
        # This "trims" the single outlier score.
        for row_index, col_label in outlier_field_labels.items():
            features.at[row_index, col_label] = np.nan
            
    # --- 2. (EXISTING) Weighted Normalized Sum Logic ---
    
    # Get the weights from config
    weights = {
        comp['label']: comp.get('weight', 1.0) 
        for comp in config.COMPARISON_FIELDS
    }
    weights_series = pd.Series(weights)
    
    # Calculate the weighted scores (score * weight)
    # This will now ignore the np.nan values we just added
    weighted_features = features * weights_series
    
    # Sum the weighted scores for available (non-NaN) fields
    sum_scores = weighted_features.sum(axis=1)
    
    # Sum the *weights* of the available (non-NaN) fields
    available_weights_features = features.notna() * weights_series
    count_scores = available_weights_features.sum(axis=1)
    
    # Get the total possible weight (max score)
    num_total_fields = weights_series.sum()
    
    # Calculate the normalized weighted sum
    normalized_sum = (sum_scores / count_scores).fillna(0) * num_total_fields
    
    # Classify and return the passing scores
    matches = normalized_sum >= threshold
    return normalized_sum[matches]