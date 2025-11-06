# main.py
"""
Main entry point for the crawling pipeline.
Orchestrates the crawling, PageRank, and monitoring process.
"""

import time
import sys
from crawler import Crawler
from pagerank import calculate_pagerank
from fetcher import find_start_page_id
# Import both new functions
from visualizer import save_dashboard_html, save_interactive_graph
from logger import logger

# --- Monitoring Intervals (in seconds) ---
P1_INTERVAL = 1
P2_INTERVAL = 2
P3_INTERVAL = 3
VIZ_UPDATE_JSON_INTERVAL = 5 # Re-generate the HTML viz every 5 seconds
BASE_SLEEP = 1

def main():
    logger.info("=== Crawler Pipeline Started ===")
    
    start_page_id = find_start_page_id()
    if not start_page_id:
        logger.error("Could not find a start page ID. Exiting.")
        sys.exit(1)
    
    crawler = Crawler(start_page_id=start_page_id)
    
    # --- Phase 1: Discovery Crawl ---
    crawler.discovery_crawl(max_pages=5000)
    if not crawler.graph:
        logger.error("No pages were discovered. Exiting.")
        return
    logger.info(f"Discovered graph with {len(crawler.graph)} nodes.")

    # --- Initial PageRank & Viz ---
    ranks = calculate_pagerank(crawler.graph)
    
    # Generate BOTH files
    save_dashboard_html(crawler.graph, ranks, crawler.node_history, "dashboard.html")
    save_interactive_graph(crawler.graph, ranks, crawler.node_history, "graph.html")
    
    logger.info("--- Your dashboard is at 'dashboard.html' ---")
    logger.info("--- Your graph is at 'graph.html' ---")

    # --- Set Monitoring Priorities ---
    crawler.set_monitoring_priorities(ranks)

    # --- Phase 3: Monitoring Loop ---
    logger.info("=== Entering Priority Monitoring Mode (Press Ctrl+C to stop) ===")
    
    last_p1_check = last_p2_check = last_p3_check = 0.0
    last_viz_update = time.time()
    
    try:
        while True:
            current_time = time.time()
            
            if (current_time - last_p1_check) > P1_INTERVAL:
                logger.info("--- Starting P1 (High) Monitoring Sweep ---")
                crawler.monitor_pages(crawler.p1_pages)
                last_p1_check = time.time()

            if (current_time - last_p2_check) > P2_INTERVAL:
                logger.info("--- Starting P2 (Medium) Monitoring Sweep ---")
                crawler.monitor_pages(crawler.p2_pages)
                last_p2_check = time.time()

            if (current_time - last_p3_check) > P3_INTERVAL:
                logger.info("--- Starting P3 (Low) Monitoring Sweep ---")
                crawler.monitor_pages(crawler.p3_pages)
                last_p3_check = time.time()

            # Check if we should update the visualizations
            if (current_time - last_viz_update) > VIZ_UPDATE_JSON_INTERVAL:
                logger.info("--- Regenerating dashboard and graph with new analytics ---")
                fresh_ranks = calculate_pagerank(crawler.graph)
                
                # Regenerate BOTH files
                save_dashboard_html(crawler.graph, fresh_ranks, crawler.node_history, "dashboard.html")
                save_interactive_graph(crawler.graph, fresh_ranks, crawler.node_history, "graph.html")
                
                last_viz_update = time.time()

            time.sleep(BASE_SLEEP)

    except KeyboardInterrupt:
        logger.info("\n=== Crawler Pipeline Stopped by User ===")
    
    finally:
        # --- Final Save ---
        logger.info("Generating final report, dashboard, and graph...")
        final_ranks = calculate_pagerank(crawler.graph)
        
        # Save BOTH files one last time
        save_dashboard_html(crawler.graph, final_ranks, crawler.node_history, "dashboard.html")
        save_interactive_graph(crawler.graph, final_ranks, crawler.node_history, "graph.html")
        
        logger.info("Final report:")
        logger.info(f"Total pages discovered: {len(crawler.visited)}")
        logger.info("Total node versions tracked per page (showing top 10 most active):")
        
        sorted_history = sorted(crawler.node_history.items(), 
                                key=lambda item: len(item[1]), 
                                reverse=True)
        
        for i, (page_id, history) in enumerate(sorted_history):
            if i < 10:
                logger.info(f"  Page {page_id:<15}: {len(history)} versions")
        if len(sorted_history) > 10:
            logger.info(f"  ... and {len(sorted_history) - 10} more pages.")

if __name__ == "__main__":
    main()