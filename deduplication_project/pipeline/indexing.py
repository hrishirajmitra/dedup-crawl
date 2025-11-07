# --- File: pipeline/indexing.py ---

import recordlinkage
import config

def create_candidate_pairs(df, block_config):
    """
    Creates candidate pairs using a fast and scalable
    "hybrid" blocking/sorting strategy.
    
    This is the most robust method:
    1. It 'blocks' on postcode_trunc for speed.
    2. It 'sorts' on name within that block to catch typos.
    """
    
    # --- Pass 1: (Postcode Block + Surname Sort) ---
    # Catches most normal pairs with typos
    print("Running Pass 1: Blocking on 'postcode_trunc', sorting on 'surname'...")
    indexer_pass1 = recordlinkage.Index()
    # Block on postcode, then sort by surname within that block
    indexer_pass1.sortedneighbourhood(
        left_on='surname', 
        block_on='postcode_trunc',
        window=config.SORTING_WINDOW_SIZE 
    )
    pairs_pass1 = indexer_pass1.index(df)
    print(f"Pass 1 found {len(pairs_pass1)} pairs.")
    
    # --- Pass 2: (Postcode Block + Given Name Sort) ---
    # Catches swapped name pairs
    print("Running Pass 2: Blocking on 'postcode_trunc', sorting on 'given_name'...")
    indexer_pass2 = recordlinkage.Index()
    # Block on postcode, then sort by given_name within that block
    indexer_pass2.sortedneighbourhood(
        left_on='given_name', 
        block_on='postcode_trunc',
        window=config.SORTING_WINDOW_SIZE
    )
    pairs_pass2 = indexer_pass2.index(df)
    print(f"Pass 2 found {len(pairs_pass2)} pairs.")
    
    # --- Pass 3: (SSN Sort) ---
    # Catches pairs with similar SSNs but different names/postcodes
    print(f"Running Pass 3: SortedNeighbourhood on 'soc_sec_id' (window={config.SORTING_WINDOW_SIZE})...")
    indexer_pass3 = recordlinkage.Index()
    indexer_pass3.sortedneighbourhood(
        left_on='soc_sec_id', 
        window=config.SORTING_WINDOW_SIZE
    )
    pairs_pass3 = indexer_pass3.index(df)
    print(f"Pass 3 found {len(pairs_pass3)} pairs.")

    # --- 4. Combine all results (union) ---
    print("Combining pairs from all 3 passes...")
    candidate_pairs = pairs_pass1.union(pairs_pass2).union(pairs_pass3)
    
    return candidate_pairs