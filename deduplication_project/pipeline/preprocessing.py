# --- File: pipeline/preprocessing.py ---

import pandas as pd
import numpy as np
from recordlinkage.preprocessing import clean

def load_and_clean_data(filepath):
    """
    Loads and cleans data.
    - Creates 'name_1' and 'name_2' (canonical, alphabetized names)
      to solve the swapped-name problem during preprocessing.
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
    fields_to_clean = [
            'given_name', 'surname', 'street_number', 'address_1', 'address_2',
            'suburb', 'postcode', 'state', 'date_of_birth', 'soc_sec_id'
        ]
    for col in fields_to_clean:
        if col in df.columns:
            df[col] = clean(df[col].astype(str))
    
    # --- (NEW) Create Canonical Name Columns ---
    print("Creating canonical name fields (name_1, name_2)...")
    if 'given_name' in df.columns and 'surname' in df.columns:
        # Stack the two columns, sort them at the row level, and unstack
        names_stacked = df[['given_name', 'surname']].stack()
        names_sorted = names_stacked.groupby(level=0).apply(np.sort)
        
        # Create the new columns
        df['name_1'] = names_sorted.str[0]
        df['name_2'] = names_sorted.str[1]
    else:
        print("Warning: 'given_name' or 'surname' not found. Cannot create canonical names.")

    # Fill any remaining NaNs with empty strings
    df = df.fillna("")
    
    return df