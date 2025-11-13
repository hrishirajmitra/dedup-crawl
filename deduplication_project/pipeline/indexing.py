# --- File: pipeline/indexing.py ---

import recordlinkage
import config

def create_candidate_pairs(df, block_config):
    """
    Creates candidate pairs using the "Slow & Accurate"
    4-pass "OR" (union) logic.
    
    1. Blocks on 'surname_trunc' (catches normal pairs)
    2. Blocks on 'given_name_trunc' (catches swapped names)
    3. Sorts on 'soc_sec_id' (catches pairs with similar SSNs)
    4. Sorts on 'postcode' (catches pairs with similar postcodes)
    """
    
    # --- Pass 1: Block on surname_trunc ---
    print("Running Pass 1: Blocking on 'surname_trunc'...")
    indexer_pass1 = recordlinkage.Index()
    indexer_pass1.block(on='surname_trunc')
    pairs_pass1 = indexer_pass1.index(df)
    print(f"Pass 1 found {len(pairs_pass1)} pairs.")
    
    # --- Pass 2: Block on given_name_trunc ---
    print("Running Pass 2: Blocking on 'given_name_trunc'...")
    indexer_pass2 = recordlinkage.Index()
    indexer_pass2.block(on='given_name_trunc')
    pairs_pass2 = indexer_pass2.index(df)
    print(f"Pass 2 found {len(pairs_pass2)} pairs.")
    
    # --- Pass 3: Sort on soc_sec_id ---
    print(f"Running Pass 3: SortedNeighbourhood on 'soc_sec_id' (window={config.SORTING_WINDOW_SIZE})...")
    indexer_pass3 = recordlinkage.Index()
    indexer_pass3.sortedneighbourhood(
        left_on='soc_sec_id', 
        window=config.SORTING_WINDOW_SIZE
    )
    pairs_pass3 = indexer_pass3.index(df)
    print(f"Pass 3 found {len(pairs_pass3)} pairs.")

    # --- Pass 4: Sort on postcode ---
    print(f"Running Pass 4: SortedNeighbourhood on 'postcode' (window={config.POSTCODE_SORTING_WINDOW_SIZE})...")
    indexer_pass4 = recordlinkage.Index()
    indexer_pass4.sortedneighbourhood(
        left_on='postcode', 
        window=config.POSTCODE_SORTING_WINDOW_SIZE
    )
    pairs_pass4 = indexer_pass4.index(df)
    print(f"Pass 4 found {len(pairs_pass4)} pairs.")

    # --- 5. Combine all results (union) ---
    print("Combining pairs from all 4 passes...")
    candidate_pairs = pairs_pass1.union(pairs_pass2).union(pairs_pass3).union(pairs_pass4)
    
    return candidate_pairs