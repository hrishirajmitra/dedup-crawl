# --- File: main.py ---

import time
import pandas as pd
import config
from pipeline import preprocessing, indexing, comparison, classification

def run_pipeline():
    """
    Executes the full deduplication pipeline from start to finish.
    """
    print("--- Starting Deduplication Pipeline ---")
    start_time = time.time()

    # --- 1. Preprocessing ---
    print(f"Loading and cleaning {config.INPUT_FILE}...")
    df = preprocessing.load_and_clean_data(config.INPUT_FILE)
    if df is None:
        return
    print(f"Data loaded. Shape: {df.shape}")

    # --- 2. Indexing ---
    print(f"Creating candidate pairs...")
    # Call the new indexer, which no longer needs a 'block_field' key
    candidate_pairs = indexing.create_candidate_pairs(df, None) # <-- MODIFIED
    print(f"Found {len(candidate_pairs)} potential pairs for comparison.")

    # --- 3. Comparison ---
    print("Comparing features for candidate pairs...")
    features = comparison.compare_pairs(candidate_pairs, df, config.COMPARISON_FIELDS)
    print("Feature comparison complete.")
    
    # --- 4. Classification ---
    print(f"Classifying duplicates with total score >= {config.CLASSIFICATION_THRESHOLD}...")
    duplicate_pairs = classification.find_duplicates(features, config.CLASSIFICATION_THRESHOLD)
    print(f"** Found {len(duplicate_pairs)} duplicate pairs. **")

    # --- 5. Save Results ---
    print(f"Saving results to {config.RESULTS_FILE}...")
    try:
        # Convert MultiIndex to a readable DataFrame
        duplicate_pairs_df = pd.DataFrame(index=duplicate_pairs).reset_index()
        
        # Standardize column names
        if len(duplicate_pairs_df.columns) >= 2:
            new_cols = ['level_0', 'level_1'] + list(duplicate_pairs_df.columns[2:])
            duplicate_pairs_df.columns = new_cols
        else:
            print("Error: Results DataFrame has fewer than 2 columns.")

        duplicate_pairs_df.to_csv(config.RESULTS_FILE, index=False)
        
    except Exception as e:
        print(f"Error saving results: {e}")

    end_time = time.time()
    print(f"--- Pipeline finished in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    run_pipeline()