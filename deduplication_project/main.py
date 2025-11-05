# --- File: main.py ---

import time
import pandas as pd
import config
from pipeline import preprocessing, indexing, comparison, classification


def save_results(duplicate_pairs, output_file):
    """Save duplicate pairs to CSV file."""
    duplicate_pairs_df = pd.DataFrame(index=duplicate_pairs).reset_index()
    duplicate_pairs_df.columns = ['level_0', 'level_1'] + list(duplicate_pairs_df.columns[2:])
    duplicate_pairs_df.to_csv(output_file, index=False)


def run_pipeline():
    """Executes the full deduplication pipeline from start to finish."""
    start_time = time.time()
    
    df = preprocessing.load_and_clean_data(config.INPUT_FILE)
    candidate_pairs = indexing.create_candidate_pairs(df, None)
    features = comparison.compare_pairs(candidate_pairs, df, config.COMPARISON_FIELDS)
    duplicate_pairs = classification.find_duplicates(features, config.CLASSIFICATION_THRESHOLD)
    save_results(duplicate_pairs, config.RESULTS_FILE)
    
    elapsed_time = time.time() - start_time
    print(f"\nFound {len(duplicate_pairs):,} duplicate pairs in {elapsed_time:.2f}s")


if __name__ == "__main__":
    run_pipeline()