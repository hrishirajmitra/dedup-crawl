# --- File: cluster_results.py ---

import pandas as pd
import networkx as nx
import config

def generate_cluster_report():
    """
    Loads all records and the found pairs, then joins them
    to create a single report sorted by group size (largest first).
    """
    
    # --- 1. Load the original data ---
    try:
        df_data = pd.read_csv(config.INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: Original data file '{config.INPUT_FILE}' not found.")
        return

    # Set the correct index for joining
    if 'rec_id' in df_data.columns:
        df_data = df_data.set_index('rec_id')
    elif 'Unnamed: 0' in df_data.columns:
        df_data = df_data.set_index('Unnamed: 0')
        df_data.index.name = 'rec_id'
    else:
        df_data = df_data.reset_index().rename(columns={"index": "rec_id"})
        df_data = df_data.set_index('rec_id')
        
    all_record_ids = df_data.index.tolist()

    # --- 2. Load the found duplicate pairs ---
    try:
        df_pairs = pd.read_csv(config.RESULTS_FILE)
    except FileNotFoundError:
        print(f"Error: Results file '{config.RESULTS_FILE}' not found.")
        print("Please run 'main.py' first.")
        return

    # --- 3. Build the graph and find ALL clusters ---
    print("Building graph...")
    G = nx.Graph()
    G.add_nodes_from(all_record_ids)  # Add all 5,000 nodes
    G.add_edges_from(df_pairs.values)  # Add the duplicate-pair edges
    
    clusters = list(nx.connected_components(G))
    print(f"Found {len(clusters)} total groups (including unique records).")

    # --- 4. Create a mapping from record_id to 'Person' label ---
    id_to_group_map = {}
    for i, cluster_ids in enumerate(clusters):
        group_label = f"Person {i + 1}"
        for record_id in cluster_ids:
            id_to_group_map[record_id] = group_label
            
    cluster_series = pd.Series(id_to_group_map, name="person_group")
    
    # --- 5. Join the group label to the original data ---
    df_report = df_data.join(cluster_series)
    
    # --- 6. (NEW) Calculate and add group size ---
    # Count the occurrences of each person_group and map it
    group_sizes = df_report['person_group'].map(df_report['person_group'].value_counts())
    df_report['group_size'] = group_sizes
    
    # --- 7. (MODIFIED) Sort for readability ---
    # Sort by group_size (descending), then person_group (ascending)
    df_report = df_report.sort_values(
        by=['group_size', 'person_group', df_report.index.name],
        ascending=[False, True, True]
    )
    
    # Re-order columns to put 'person_group' and 'group_size' first
    cols = df_report.columns.tolist()
    cols.remove('person_group')
    cols.remove('group_size')
    final_cols = ['person_group', 'group_size'] + cols
    df_report = df_report[final_cols]
    
    # --- 8. Save the final report ---
    OUTPUT_FILE = "full_cluster_report_sorted.csv"
    try:
        df_report.to_csv(OUTPUT_FILE, index_label="record_id")
        print(f"Successfully saved full report to '{OUTPUT_FILE}'.")
    except Exception as e:
        print(f"Error saving file: {e}")


if __name__ == "__main__":
    print("--- Starting Full Cluster Report Generation ---")
    generate_cluster_report()
    print("--- Report Generation Finished ---")