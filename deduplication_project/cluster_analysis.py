# --- File: analyze_cluster_quality.py ---

import pandas as pd
import numpy as np
import config

# --- Input Files ---
CLUSTER_REPORT_FILE = "full_cluster_report_sorted.csv"
PAIRS_FILE = "found_duplicate_pairs.csv"

# --- Output File ---
ANALYSIS_FILE = "cluster_quality_analysis.csv"

def run_quality_analysis():
    """
    Reads the final cluster report and the pairs file
    to generate group-wise statistics on link score
    and link density (cohesion).
    """
    print(f"--- Analyzing Cluster Quality (Cohesion) ---")
    
    # --- 1. Load Cluster Report ---
    try:
        df_report = pd.read_csv(CLUSTER_REPORT_FILE, index_col='record_id')
    except FileNotFoundError:
        print(f"Error: Report file '{CLUSTER_REPORT_FILE}' not found.")
        print("Please run 'cluster_results.py' first.")
        return
    
    # --- 2. Load Pairs with Scores ---
    try:
        df_pairs = pd.read_csv(PAIRS_FILE)
    except FileNotFoundError:
        print(f"Error: Pairs file '{PAIRS_FILE}' not found.")
        print("Please run 'main.py' first.")
        return

    # --- 3. Focus on Duplicate Groups ---
    df_dupes = df_report[df_report['group_size'] > 1]
    if df_dupes.empty:
        print("No duplicate groups found to analyze.")
        return
        
    # --- 4. Map Groups to Pairs ---
    # Create a map: 'rec-123' -> 'Person 1'
    id_to_group_map = df_dupes['person_group'].to_dict()
    
    # Map group names to both sides of the pairs
    df_pairs['group_left'] = df_pairs['level_0'].map(id_to_group_map)
    df_pairs['group_right'] = df_pairs['level_1'].map(id_to_group_map)
    
    # Filter for intra-cluster links (where both records are in the same group)
    df_internal_links = df_pairs[
        df_pairs['group_left'] == df_pairs['group_right']
    ].copy()
    
    # Drop links that weren't in a duplicate group (NaN)
    df_internal_links = df_internal_links.dropna(subset=['group_left'])
    df_internal_links.rename(columns={'group_left': 'person_group'}, inplace=True)

    if df_internal_links.empty:
        print("No internal links found for duplicate groups.")
        return

    # --- 5. Aggregate Similarity Stats ---
    print("Calculating group-wise similarity statistics...")
    group_stats = df_internal_links.groupby('person_group')['score'].agg(
        avg_score='mean',
        min_score='min',
        max_score='max',
        num_links_found='count'
    ).reset_index()
    
    # --- 6. Get Group Sizes ---
    group_sizes = df_dupes.groupby('person_group').size().to_frame('group_size').reset_index()
    
    # --- 7. Combine Stats and Calculate Density ---
    df_analysis = pd.merge(group_sizes, group_stats, on='person_group', how='left')
    
    # Calculate max possible links: n * (n-1) / 2
    df_analysis['num_links_possible'] = df_analysis['group_size'] * (df_analysis['group_size'] - 1) / 2
    
    # Calculate density (handle divide-by-zero for size=2 groups)
    # A size 2 group has 1 possible link.
    df_analysis.loc[df_analysis['group_size'] == 2, 'num_links_possible'] = 1
    
    df_analysis['link_density'] = (
        df_analysis['num_links_found'] / df_analysis['num_links_possible']
    ).fillna(0)
    
    # --- 8. Final Sort and Report ---
    # Sort by the most "risky" groups: low score, low density
    df_analysis = df_analysis.sort_values(by=['avg_score', 'link_density'], ascending=[True, True])
    
    # Round for readability
    df_analysis = df_analysis.round(2)
    
    print("\n###Overall Cluster Quality ###")
    print(f"Total duplicate groups:  {len(df_analysis)}")
    print(f"Overall avg. similarity: {df_analysis['avg_score'].mean():.2f}")
    print(f"Overall avg. link density: {df_analysis['link_density'].mean():.2f}")

    # Save to CSV
    try:
        df_analysis.to_csv(ANALYSIS_FILE, index=False)
        print(f"\nSuccessfully saved detailed analysis to '{ANALYSIS_FILE}'.")
    except Exception as e:
        print(f"Error saving analysis file: {e}")
        
    # Print a sample to console
    print("\n### Sample: 10 'Weakest' Clusters (by Avg. Score) ###")
    print(df_analysis.head(10).to_string(index=False))

if __name__ == "__main__":
    run_quality_analysis()