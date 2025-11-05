# --- File: config.py ---

# File configuration
INPUT_FILE = "dedup_data.csv"
RESULTS_FILE = "found_duplicate_pairs.csv"

# --- (NEW) Indexing Configuration ---
# 'window_size' is for Sorted Neighbourhood. It compares each
# record with its 'n' closest neighbors after sorting.
# A small window (3-5) is very fast and catches most typos.
SORTING_WINDOW_SIZE = 9

# Comparison fields and methods
# This advanced structure is still needed.
COMPARISON_FIELDS = [
    # Normal comparisons
    {"field": "given_name", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "given_name"},
    {"field": "surname",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "surname"},
    {"field": "address_1",  "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_1"},
    {"field": "suburb",     "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.85, "label": "suburb"},
    {"field": "state",      "method": "exact", "label": "state"},
    
    # Crossed-field comparisons
    {"field_left": "given_name", "field_right": "surname", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "gv_vs_sn"},
     
    {"field_left": "surname", "field_right": "given_name", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "sn_vs_gv"}
]

# Classification configuration
# Your best threshold was 3.0, which should work well here.
CLASSIFICATION_THRESHOLD = 3.0