# --- File: pipeline/indexing.py ---

import recordlinkage

def create_candidate_pairs(df, block_field):
    """
    Creates candidate pairs for comparison using blocking.
    
    This avoids an N*N comparison, which is computationally expensive.
    We only compare records that match on the 'block_field'.
    """
    indexer = recordlinkage.Index()
    
    # 'block' is a simple and effective indexing method
    indexer.block(block_field)
    
    candidate_pairs = indexer.index(df)
    
    return candidate_pairs