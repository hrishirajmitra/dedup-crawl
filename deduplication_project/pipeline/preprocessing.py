# --- File: pipeline/preprocessing.py ---

import pandas as pd
import numpy as np
from recordlinkage.preprocessing import clean

def load_and_clean_data(filepath):
    """
    Loads and cleans data.
    - Manually cleans only non-null values to preserve NaNs.
    - Creates 'trunc' (truncated) fields for indexing.
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
        df = df.reset_index().rename(columns={"index": "rec_id"})
        df = df.set_index('rec_id')

    # --- Standardize column names ---
    df.columns = [c.lower().strip() for c in df.columns]

    # --- Clean data in relevant fields ---
    fields_to_clean = [
        'given_name', 'surname', 'street_number', 'address_1', 'address_2',
        'suburb', 'postcode', 'state', 'date_of_birth', 'soc_sec_id'
    ]
    
    for col in fields_to_clean:
        if col in df.columns:
            non_null_mask = df[col].notna()
            df.loc[non_null_mask, col] = clean(df.loc[non_null_mask, col].astype(str))

    # --- Create Truncated Indexing Keys ---
    print("Creating truncated keys for indexing...")
    
    def get_trunc(name, length=4):
        if pd.isna(name):
            return np.nan
        return str(name)[:length]

    if 'given_name' in df.columns:
        df['given_name_trunc'] = df['given_name'].apply(get_trunc)
    if 'surname' in df.columns:
        df['surname_trunc'] = df['surname'].apply(get_trunc)
        
    return df