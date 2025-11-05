# --- File: pipeline/indexing.py ---

import recordlinkage
import config

def create_candidate_pairs(df, block_config):
    """
    Creates candidate pairs using a fast and typo-robust
    "Sorted Neighbourhood" strategy.

    This is highly scalable and replaces the 'block' method.
    """
    
    window_size = config.SORTING_WINDOW_SIZE
    
    # --- Pass 1: Sort by surname, check neighbors ---
    print(f"Running Pass 1: SortedNeighbourhood on 'surname' (window={window_size})...")
    indexer_pass1 = recordlinkage.Index()
    indexer_pass1.sortedneighbourhood(left_on='surname', window=window_size)
    pairs_pass1 = indexer_pass1.index(df)
    print(f"Pass 1 found {len(pairs_pass1)} pairs.")
    
    # --- Pass 2: Sort by given_name, check neighbors ---
    print(f"Running Pass 2: SortedNeighbourhood on 'given_name' (window={window_size})...")
    indexer_pass2 = recordlinkage.Index()
    indexer_pass2.sortedneighbourhood(left_on='given_name', window=window_size)
    pairs_pass2 = indexer_pass2.index(df)
    print(f"Pass 2 found {len(pairs_pass2)} pairs.")
    
    # --- 3. Combine the results (union) ---
    print(f"Combining pairs...")
    candidate_pairs = pairs_pass1.union(pairs_pass2)
    
    return candidate_pairs