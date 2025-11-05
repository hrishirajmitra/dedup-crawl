# --- File: pipeline/indexing.py ---

import recordlinkage
import config
from . import constants as const


def create_candidate_pairs(df, block_config):
    """
    Creates candidate pairs using Sorted Neighbourhood on the
    new 'name_1' and 'name_2' canonical fields.
    
    This is fast, scalable, and robust to both typos AND
    swapped names.
    """
    window_size = config.SORTING_WINDOW_SIZE
    
    # Pass 1: Sort by name_1 (alphabetically first name)
    print(f"Running Pass 1: SortedNeighbourhood on '{const.NAME_1_FIELD}' (window={window_size})...")
    indexer_pass1 = recordlinkage.Index()
    indexer_pass1.sortedneighbourhood(left_on=const.NAME_1_FIELD, window=window_size)
    pairs_pass1 = indexer_pass1.index(df)
    print(f"Pass 1 found {len(pairs_pass1)} pairs.")
    
    # Pass 2: Sort by name_2 (alphabetically second name)
    print(f"Running Pass 2: SortedNeighbourhood on '{const.NAME_2_FIELD}' (window={window_size})...")
    indexer_pass2 = recordlinkage.Index()
    indexer_pass2.sortedneighbourhood(left_on=const.NAME_2_FIELD, window=window_size)
    pairs_pass2 = indexer_pass2.index(df)
    print(f"Pass 2 found {len(pairs_pass2)} pairs.")
    
    # Combine the results (union)
    print("Combining pairs...")
    candidate_pairs = pairs_pass1.union(pairs_pass2)
    
    return candidate_pairs