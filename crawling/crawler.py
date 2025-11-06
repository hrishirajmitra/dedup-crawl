# crawler.py
"""
Defines the main Crawler class.
"""

import numpy as np
from collections import deque
from typing import Deque, Set, Dict, List, Any
from logger import logger
from fetcher import fetch_page

class Crawler:
    def __init__(self, start_page_id: str):
        """Initializes the crawler's state."""
        self.start_page_id = start_page_id
        
        # For BFS discovery
        self.frontier: Deque[str] = deque([start_page_id])
        self.visited: Set[str] = set()
        
        # --- Data to be collected ---
        self.graph: Dict[str, List[str]] = {} 
        self.node_states: Dict[str, str] = {}
        self.node_history: Dict[str, List[Dict]] = {} 
        
        # --- Priority Monitoring Lists ---
        self.p1_pages: List[str] = [] # High priority
        self.p2_pages: List[str] = [] # Medium priority
        self.p3_pages: List[str] = [] # Low priority
        
        logger.info(f"Crawler initialized with start page {start_page_id}.")

    def _process_page_data(self, page_data: Dict[str, Any]):
        """
        Internal helper to process data from a fetched page.
        """
        page_id = page_data.get("page_id")
        if not page_id:
            logger.warning("Fetched page has no 'page_id', skipping.")
            return

        # Objective 2: Update graph structure
        self.graph[page_id] = page_data.get("outgoing_links", [])

        # Objective 3: Track node ID updates
        current_node_id = page_data.get("node_id")
        last_known_node_id = self.node_states.get(page_id)

        if last_known_node_id != current_node_id:
            if last_known_node_id:
                logger.info(f"NODE UPDATE: Page {page_id} changed from "
                            f"{last_known_node_id} -> {current_node_id}")
            else:
                logger.info(f"Discovered Page {page_id} (Node: {current_node_id})")
            
            self.node_states[page_id] = current_node_id
            self.node_history[page_id] = page_data.get("node_history", [])

    def discovery_crawl(self, max_pages: int = 1000):
        """
        Phase 1: Performs a BFS crawl to discover the site structure.
        """
        logger.info("--- Starting Discovery Crawl ---")
        pages_visited = 0
        
        while self.frontier and pages_visited < max_pages:
            current_page_id = self.frontier.popleft()
            
            if current_page_id in self.visited:
                continue
                
            page_data = fetch_page(current_page_id)
            if not page_data:
                continue 
                
            self.visited.add(current_page_id)
            pages_visited += 1
            
            self._process_page_data(page_data)
            
            for link in self.graph.get(current_page_id, []):
                if link not in self.visited:
                    self.frontier.append(link)
                            
        logger.info(f"Discovery crawl finished. Visited {len(self.visited)} pages.")

    def set_monitoring_priorities(self, ranks: Dict[str, float]):
        """
        Uses PageRank scores to sort pages into priority buckets.
        """
        if not ranks:
            logger.warning("No ranks provided. Using equal priority for all pages.")
            self.p2_pages = list(self.visited) # Put all in medium priority
            return
            
        # Get ranks for pages we've actually visited
        visited_ranks = {page: ranks.get(page, 0) for page in self.visited}
        
        # Sort pages by rank, descending
        sorted_pages = sorted(visited_ranks.items(), key=lambda item: item[1], reverse=True)
        
        # Use quantiles to create 3 buckets (e.g., top 20%, middle 50%, low 30%)
        # This is a robust way to divide them.
        rank_values = np.array([r for r in visited_ranks.values() if r > 0])
        if len(rank_values) < 3:
             self.p2_pages = list(self.visited) # Not enough data, put all in medium
             return

        q_high = np.quantile(rank_values, 0.80) # Top 20%
        q_low = np.quantile(rank_values, 0.30)  # Bottom 30%

        for page, rank in sorted_pages:
            if rank >= q_high:
                self.p1_pages.append(page)
            elif rank < q_low:
                self.p3_pages.append(page)
            else:
                self.p2_pages.append(page)
        
        logger.info(f"Monitoring priorities set: "
                    f"P1 (High): {len(self.p1_pages)} pages, "
                    f"P2 (Medium): {len(self.p2_pages)} pages, "
                    f"P3 (Low): {len(self.p3_pages)} pages")

    def monitor_pages(self, pages_to_check: List[str]) -> int:
        """
        Re-visits a specific list of pages to check for node_id updates.
        Returns the number of updates found.
        """
        if not pages_to_check:
            return 0
            
        updates_found = 0
        
        for page_id in pages_to_check:
            page_data = fetch_page(page_id)
            if page_data:
                old_node_id = self.node_states.get(page_id)
                self._process_page_data(page_data)
                
                if old_node_id != self.node_states.get(page_id):
                    updates_found += 1
        
        logger.info(f"Monitoring sweep finished for {len(pages_to_check)} pages. "
                    f"Found {updates_found} updates.")
        return updates_found