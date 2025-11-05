# --- File: cluster_results.py ---

import pandas as pd
import networkx as nx
import config

def generate_cluster_report():
    """
    Loads all records and the found pairs, filters pairs by a
    "strength" threshold, and then groups all records into
    clusters, sorting the final report by group size.
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
    original_index_name = df_data.index.name # Store for sorting

    # --- 2. Load the found duplicate pairs (with scores) ---
    try:
        df_pairs = pd.read_csv(config.RESULTS_FILE)
    except FileNotFoundError:
        print(f"Error: Results file '{config.RESULTS_FILE}' not found.")
        print("Please run 'main.py' first.")
        return
    except Exception as e:
        print(f"Error reading {config.RESULTS_FILE}: {e}")
        return

    # --- 3. Filter for "Strong" Links ---
    clustering_threshold = getattr(config, 'CLUSTERING_THRESHOLD', config.CLASSIFICATION_THRESHOLD)
    
    strong_links_df = df_pairs[df_pairs['score'] >= clustering_threshold]
    print(f"Total pairs found: {len(df_pairs)}")
    print(f"Using cluster threshold: {clustering_threshold}")
    print(f"Filtered down to {len(strong_links_df)} strong links for clustering.")

    # --- 4. Build the graph and find ALL clusters ---
    print("Building graph...")
    G = nx.Graph()
    G.add_nodes_from(all_record_ids) # Add all 5,000 nodes
    
    # Add edges *only* from the strong pairs
    G.add_edges_from(strong_links_df[['level_0', 'level_1']].values)
    
    clusters = list(nx.connected_components(G))
    print(f"Found {len(clusters)} total groups (including unique records).")

    # --- 5. Create a mapping from record_id to a numeric cluster_id ---
    # We use a numeric ID first for correct sorting
    id_to_cluster_map = {}
    for i, cluster_ids in enumerate(clusters):
        cluster_id = i + 1  # Create a simple numeric ID
        for record_id in cluster_ids:
            id_to_cluster_map[record_id] = cluster_id
            
    cluster_series = pd.Series(id_to_cluster_map, name="cluster_id")
    
    # --- 6. Join the group label to the original data ---
    df_report = df_data.join(cluster_series)
    
    # --- 7. Calculate and add group size ---
    group_sizes = df_report['cluster_id'].map(df_report['cluster_id'].value_counts())
    df_report['group_size'] = group_sizes
    
    # --- 8. Sort by group size (desc) and numeric ID (asc) ---
    df_report = df_report.sort_values(
        by=['group_size', 'cluster_id', original_index_name],
        ascending=[False, True, True]
    )
    
    # --- 9. Create the final "Person" label (after sorting) ---
    # Create a map from the numeric cluster_id to the "Person X" label
    # This ensures "Person 1" is the largest group, "Person 2" is the next, etc.
    cluster_id_to_person_label = {
        cid: f"Person {i+1}" 
        for i, cid in enumerate(df_report['cluster_id'].unique())
    }
    
    df_report['person_group'] = df_report['cluster_id'].map(cluster_id_to_person_label)
    
    # --- 10. Finalize and Save ---
    # Re-order columns to put 'person_group' and 'group_size' first
    cols = df_report.columns.tolist()
    cols.remove('person_group')
    cols.remove('group_size')
    cols.remove('cluster_id') # Remove the temporary numeric ID
    final_cols = ['person_group', 'group_size'] + cols
    df_report = df_report[final_cols]
    
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