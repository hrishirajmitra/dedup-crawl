# --- File: pipeline/preprocessing.py ---

import pandas as pd
import numpy as np
from recordlinkage.preprocessing import clean
from . import constants as const


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

    # Set a unique record index
    if const.FIELD_REC_ID in df.columns:
        df = df.set_index(const.FIELD_REC_ID)
    elif const.FIELD_UNNAMED_0 in df.columns:
        df = df.set_index(const.FIELD_UNNAMED_0)
        df.index.name = const.FIELD_REC_ID
    else:
        print("Warning: No clear ID column found. Using default integer index.")
        df = df.reset_index().rename(columns={"index": const.FIELD_REC_ID})
        df = df.set_index(const.FIELD_REC_ID)

    # Standardize column names
    df.columns = [c.lower().strip() for c in df.columns]

    # Clean data in relevant fields
    for col in const.FIELDS_TO_CLEAN:
        if col in df.columns:
            df[col] = clean(df[col].astype(str))
    
    # Create canonical name columns
    print(f"Creating canonical name fields ({const.NAME_1_FIELD}, {const.NAME_2_FIELD})...")
    if const.FIELD_GIVEN_NAME in df.columns and const.FIELD_SURNAME in df.columns:
        # Stack the two columns, sort them at the row level, and unstack
        names_stacked = df[[const.FIELD_GIVEN_NAME, const.FIELD_SURNAME]].stack()
        names_sorted = names_stacked.groupby(level=0).apply(np.sort)
        
        # Create the new columns
        df[const.NAME_1_FIELD] = names_sorted.str[0]
        df[const.NAME_2_FIELD] = names_sorted.str[1]
    else:
        print(f"Warning: '{const.FIELD_GIVEN_NAME}' or '{const.FIELD_SURNAME}' not found. Cannot create canonical names.")

    # Fill any remaining NaNs with empty strings
    df = df.fillna("")
    
    return df