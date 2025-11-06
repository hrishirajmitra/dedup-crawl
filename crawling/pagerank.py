# pagerank.py
"""
Contains the PageRank calculation logic.
"""

from typing import Dict, List
from config import DAMPING_FACTOR, MAX_ITERATIONS, TOLERANCE
from logger import logger

def calculate_pagerank(graph: Dict[str, List[str]]) -> Dict[str, float]:
    """
    Calculates PageRank using the iterative power method
    with the Gauss-Seidel optimization (using new values as they are computed).
    """
    logger.info("Starting PageRank calculation (Gauss-Seidel optimized)...")
    if not graph:
        logger.warning("Graph is empty. Cannot calculate PageRank.")
        return {}

    pages = list(graph.keys())
    num_pages = len(pages)
    
    # Initialize ranks
    ranks = {page: 1.0 / num_pages for page in pages}
    
    # Pre-calculate a "dangling nodes" rank contribution
    dangling_pages = {page for page in pages if not graph[page]}

    for i in range(MAX_ITERATIONS):
        old_ranks = ranks.copy()
        total_change = 0
        
        # Base rank + contribution from dangling nodes
        dangling_sum = sum(old_ranks[page] for page in dangling_pages)
        base_rank_part = (1.0 - DAMPING_FACTOR) / num_pages
        dangling_part = DAMPING_FACTOR * (dangling_sum / num_pages)
        
        for page in pages:
            rank_sum = 0
            # Calculate sum of ranks from inbound links
            for linking_page in pages:
                if page in graph[linking_page]:
                    num_links = len(graph[linking_page])
                    # Use the most recent rank value (might be from this iter)
                    rank_sum += ranks[linking_page] / num_links 
            
            new_rank = base_rank_part + dangling_part + DAMPING_FACTOR * rank_sum
            
            ranks[page] = new_rank
            total_change += abs(ranks[page] - old_ranks[page])
        
        if total_change < (TOLERANCE * num_pages):
            logger.info(f"PageRank converged after {i+1} iterations.")
            break
    else:
        logger.warning(f"PageRank did not converge after {MAX_ITERATIONS} iterations.")

    return ranks