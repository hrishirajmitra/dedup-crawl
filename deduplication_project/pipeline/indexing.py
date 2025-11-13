# --- File: pipeline/indexing.py ---

import recordlinkage
import config

def create_candidate_pairs(df, block_config):
    """
    Creates candidate pairs using a "penta-pass" OR logic.
    
    1. Blocks on 'surname_trunc'
    2. Blocks on 'given_name_trunc'
    3. Sorts on 'soc_sec_id'
    4. Sorts on 'postcode'
    5. (NEW) Sorts on 'address_1'
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

    # --- (NEW) Pass 5: Sort on address_1 ---
    print(f"Running Pass 5: SortedNeighbourhood on 'address_1' (window={config.ADDRESS_SORTING_WINDOW_SIZE})...")
    indexer_pass5 = recordlinkage.Index()
    indexer_pass5.sortedneighbourhood(
        left_on='address_1', 
        window=config.ADDRESS_SORTING_WINDOW_SIZE  # Use the new window
    )
    pairs_pass5 = indexer_pass5.index(df)
    print(f"Pass 5 found {len(pairs_pass5)} pairs.")

    # --- 6. Combine all results (union) ---
    print("Combining pairs from all 5 passes...")
    candidate_pairs = pairs_pass1.union(pairs_pass2).union(pairs_pass3).union(pairs_pass4).union(pairs_pass5)
    
    return candidate_pairs