# --- File: pipeline/preprocessing.py ---

import pandas as pd
from recordlinkage.preprocessing import clean

def load_and_clean_data(filepath):
    """
    Loads and cleans the dataset for deduplication.
    
    - Loads the CSV.
    - Sets a proper index (assumes 'rec_id' or first column is the ID).
    - Cleans and standardizes column names.
    - Cleans the text data in key fields.
    - Fills missing values to prevent errors.
    """
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}")
        return None

    # --- Set a unique record index ---
    if 'rec_id' in df.columns:
        df = df.set_index('rec_id')
    elif 'Unnamed: 0' in df.columns:
        df = df.set_index('Unnamed: 0')
        df.index.name = 'rec_id'
    else:
        print("Warning: No clear ID column found. Using default integer index.")
        df = df.reset_index().rename(columns={"index": "rec_id"})
        df = df.set_index('rec_id')

    # --- Standardize column names ---
    df.columns = [c.lower().strip() for c in df.columns]

    # --- Clean data in relevant fields ---
    fields_to_clean = ['given_name', 'surname', 'address_1', 'suburb', 'state']
    for col in fields_to_clean:
        if col in df.columns:
            # Convert to string and apply standard cleaning
            df[col] = clean(df[col].astype(str))
    
    # --- (Truncated columns are no longer needed) ---

    # Fill any remaining NaNs with empty strings
    df = df.fillna("")
    
    return df