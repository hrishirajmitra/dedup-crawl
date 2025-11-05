# --- File: main.py ---

import time
import pandas as pd
import config
from pipeline import preprocessing, indexing, comparison, classification

def run_pipeline():
    """
    Executes the full deduplication pipeline.
    """
    start_time = time.time()

    # --- 1. Preprocessing ---
    df = preprocessing.load_and_clean_data(config.INPUT_FILE)
    if df is None:
        print(f"Error: Could not load {config.INPUT_FILE}. Exiting.")
        return

    # --- 2. Indexing ---
    candidate_pairs = indexing.create_candidate_pairs(df, None)

    # --- 3. Comparison ---
    features = comparison.compare_pairs(candidate_pairs, df, config.COMPARISON_FIELDS)
    
    # --- 4. Classification ---
    # This is a Series with (pair) as index and (score) as value
    duplicate_pairs_with_scores = classification.find_duplicates(
        features, config.CLASSIFICATION_THRESHOLD
    )
    print(f"** Found {len(duplicate_pairs_with_scores)} duplicate pairs. **")

    # --- 5. Save Results (with scores) ---
    print(f"Saving results (with scores) to {config.RESULTS_FILE}...")
    try:
        # --- (MODIFIED) ---
        # Convert the Series (MultiIndex + score) to a DataFrame
        df_to_save = duplicate_pairs_with_scores.reset_index()
        
        # Name the columns correctly so evaluation.py can find them
        df_to_save.columns = ['level_0', 'level_1', 'score']
        
        # Save to CSV, *without* the new default index
        df_to_save.to_csv(config.RESULTS_FILE, index=False)
        # --- (END MODIFIED) ---
        
    except Exception as e:
        print(f"Error saving results: {e}")

    end_time = time.time()
    print(f"--- Pipeline finished in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    run_pipeline()