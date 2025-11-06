# visualizer.py
"""
Generates two separate files:
1. dashboard.html: A static HTML page with all statistics.
2. graph.html: A standalone interactive Pyvis graph.
"""

from pyvis.network import Network
from typing import Dict, List
from logger import logger
import math
import time
import os

# --- Helper functions for analytics ---

def _get_color_by_updates(update_count: int) -> str:
    if update_count <= 1: return "#3498db" # Blue (Static)
    elif update_count <= 5: return "#f1c40f" # Yellow (Warm)
    elif update_count <= 10: return "#e67e22" # Orange (Warmer)
    else: return "#e74c3c" # Red (Hot)

def _get_size_by_pagerank(rank: float, max_rank: float) -> float:
    if rank <= 0 or max_rank <= 0: return 10
    normalized_rank = rank / max_rank
    return 10 + (math.log1p(normalized_rank * 9) * 20)

def _calculate_statistics(
    graph: Dict[str, List[str]],
    ranks: Dict[str, float],
    node_history: Dict[str, List[Dict]]
) -> Dict:
    """Calculates all key statistics for the dashboard."""
    stats = {}
    
    # Overall
    stats['total_pages'] = len(graph)
    stats['total_links'] = sum(len(links) for links in graph.values())
    
    # PageRank
    if ranks:
        sorted_ranks = sorted(ranks.items(), key=lambda item: item[1], reverse=True)
        stats['top_pagerank_page'] = sorted_ranks[0][0]
        stats['top_pagerank_score'] = f"{sorted_ranks[0][1]:.4f}"
        top_5_rank_html = ""
        for page, rank in sorted_ranks[:5]:
            top_5_rank_html += f"<li><span>{page}</span><span>{rank:.4f}</span></li>"
        stats['top_5_rank_html'] = top_5_rank_html
    else:
        stats.update({'top_pagerank_page': 'N/A', 'top_pagerank_score': 'N/A', 'top_5_rank_html': '<li>No PageRank data.</li>'})

    # Activity
    if node_history:
        sorted_history = sorted(node_history.items(), key=lambda item: len(item[1]), reverse=True)
        total_updates = sum(len(h) for h in node_history.values()) - len(node_history)
        stats['most_active_page'] = sorted_history[0][0]
        stats['most_active_updates'] = len(sorted_history[0][1])
        stats['total_updates'] = max(0, total_updates)
        top_5_active_html = ""
        for page, history in sorted_history[:5]:
            updates = len(history)
            top_5_active_html += f"<li><span>{page}</span><span>{updates} versions</span></li>"
        stats['top_5_active_html'] = top_5_active_html
    else:
        stats.update({'most_active_page': 'N/A', 'most_active_updates': 0, 'total_updates': 0, 'top_5_active_html': '<li>No update data.</li>'})
        
    return stats

def _get_dashboard_template(stats: Dict) -> str:
    """Returns the HTML for the standalone statistics dashboard."""
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crawler Dashboard</title>
    <style>
        :root {{
            --bg-color: #f4f7f6; --header-bg: #ffffff; --card-bg: #ffffff;
            --border-color: #e0e0e0; --text-color: #333; --text-light: #777;
            --accent-blue: #3498db; --accent-red: #e74c3c;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg-color); color: var(--text-color); margin: 0;
        }}
        header {{
            background: var(--header-bg); border-bottom: 1px solid var(--border-color);
            padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}
        header h1 {{ margin: 0; font-size: 1.5rem; color: var(--accent-blue); }}
        .container {{ max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem; }}
        .link-card {{
            background: var(--accent-blue); color: white; border-radius: 8px;
            padding: 1.5rem 2rem; margin-bottom: 2rem; text-align: center;
        }}
        .link-card a {{
            color: white; font-size: 1.25rem; font-weight: 600; text-decoration: none;
        }}
        .link-card a:hover {{ text-decoration: underline; }}
        .grid-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
        .stats-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;
        }}
        .stat-card, .list-card {{
            background: var(--card-bg); border-radius: 8px;
            padding: 1.5rem; border: 1px solid var(--border-color);
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .stat-card .label {{
            font-size: 0.9rem; color: var(--text-light); margin-bottom: 0.25rem;
            text-transform: uppercase;
        }}
        .stat-card .value {{
            font-size: 1.75rem; font-weight: 600; color: var(--accent-blue);
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
        }}
        .stat-card .value.red {{ color: var(--accent-red); }}
        .list-card h3 {{
            font-size: 1.1rem; margin: 0 0 0.75rem 0; border-bottom: 1px solid #f0f0f0;
            padding-bottom: 0.5rem;
        }}
        .list-card ul {{ list-style: none; padding: 0; margin: 0; }}
        .list-card li {{
            display: flex; justify-content: space-between; font-size: 0.95rem;
            padding: 0.5rem 0; border-bottom: 1px solid #f0f0f0;
        }}
        .list-card li:last-child {{ border-bottom: none; }}
        .list-card li span:first-child {{ font-weight: 500; }}
        .list-card li span:last-child {{ color: var(--text-light); font-weight: 400; }}
        footer {{
            text-align: center; margin-top: 2rem; font-size: 0.8rem; color: var(--text-light);
        }}
    </style>
</head>
<body>
    <header><h1>Crawler Dashboard</h1></header>
    <div class="container">
        <div class="link-card">
            <a href="graph.html" target="_blank">
                ► Open Live Interactive Graph (graph.html)
            </a>
        </div>
        
        <div class="grid-container">
            <div>
                <h2>Overall Statistics</h2>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="label">Total Pages</div>
                        <div class="value">{stats['total_pages']}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Total Links</div>
                        <div class="value">{stats['total_links']}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Total Updates</div>
                        <div class="value red">{stats['total_updates']}</div>
                    </div>
                    <div class="stat-card">
                        <div class="label">Most Active Page</div>
                        <div class="value red" title="{stats['most_active_page']}">{stats['most_active_page']}</div>
                    </div>
                </div>
            </div>
            
            <div class="list-card">
                <h3>Top 5 Pages (PageRank)</h3>
                <ul>{stats['top_5_rank_html']}</ul>
            </div>
            
            <div class="list-card">
                <h3>Top 5 Most Active Pages</h3>
                <ul>{stats['top_5_active_html']}</ul>
            </div>
        </div>
    </div>
    <footer>
        <p>Dashboard updated: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
</body>
</html>
    """

# --- Public Function 1: Save Dashboard ---

def save_dashboard_html(
    graph: Dict[str, List[str]],
    ranks: Dict[str, float],
    node_history: Dict[str, List[Dict]],
    filename: str = "dashboard.html"
):
    """Saves the standalone statistics dashboard to an HTML file."""
    logger.info(f"Generating statistics dashboard to {filename}...")
    try:
        stats = _calculate_statistics(graph, ranks, node_history)
        final_html = _get_dashboard_template(stats)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(final_html)
        logger.info("Dashboard saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save dashboard: {e}")

# --- Public Function 2: Save Graph ---

def save_interactive_graph(
    graph: Dict[str, List[str]],
    ranks: Dict[str, float],
    node_history: Dict[str, List[Dict]],
    filename: str = "graph.html"
):
    """Saves the standalone interactive Pyvis graph to an HTML file."""
    logger.info(f"Generating interactive graph to {filename}...")
    if not graph:
        logger.warning("Graph is empty. Cannot generate visualization.")
        return

    net = Network(height="90vh", width="100%", heading="Crawler Graph", directed=True)
    max_rank = max(ranks.values()) if ranks else 0.01

    # Add Nodes
    for page_id in graph.keys():
        rank = ranks.get(page_id, 0)
        update_count = len(node_history.get(page_id, []))
        node_size = _get_size_by_pagerank(rank, max_rank)
        node_color = _get_color_by_updates(update_count)
        title = (
            f"<b>Page ID:</b> {page_id}<br>"
            f"<b>PageRank:</b> {rank:.6f}<br>"
            f"<b>Updates:</b> {update_count}"
        )
        net.add_node(
            page_id, label=page_id, value=node_size,
            color=node_color, title=title
        )

    # Add Edges
    for page, links in graph.items():
        for link in links:
            if link in graph:
                net.add_edge(page, link)

    # Configure and Save
    net.toggle_physics(True)
    net.set_options("""
    var options = {
      "physics": { "solver": "forceAtlas2Based", "forceAtlas2Based": { "avoidOverlap": 0.5 } },
      "edges": { "smooth": { "type": "curvedCW", "roundness": 0.1 }, "arrows": { "to": { "enabled": true, "scaleFactor": 0.5 } } }
    }
    """)
    try:
        net.save_graph(filename)
        logger.info("Interactive graph saved successfully.")
    except Exception as e:
        logger.error(f"Failed to save interactive graph: {e}")