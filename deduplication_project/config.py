# --- File: config.py ---

# File configuration
INPUT_FILE = "dedup_data.csv"
RESULTS_FILE = "found_duplicate_pairs.csv"

# --- Indexing Configuration ---
# This is for the 'soc_sec_id' pass
SORTING_WINDOW_SIZE = 5

# This is for the 'postcode' pass
POSTCODE_SORTING_WINDOW_SIZE = 5

# Comparison fields and methods
# (This section remains unchanged, with all your weights)
COMPARISON_FIELDS = [
    {"field": "given_name", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "given_name", "weight": 1},
    {"field": "surname",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "surname", "weight": 1},
    
    # Crossed-field comparisons
    {"field_left": "given_name", "field_right": "surname", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "gv_vs_sn", "weight": 2.0},
     
    {"field_left": "surname", "field_right": "given_name", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "sn_vs_gv", "weight": 2.0},

    {"field": "soc_sec_id",    "method": "string", "string_method": "jarowinkler", "threshold": 0.90, "label": "soc_sec_id", "weight": 3.0},
    {"field": "date_of_birth", "method": "string", "string_method": "jarowinkler", "threshold": 0.90, "label": "date_of_birth", "weight": 3.0},

    {"field": "address_1", "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_1", "weight": 1.0},
    {"field": "postcode",  "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "postcode",  "weight": 1.0},
    {"field": "street_number", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "street_number", "weight": 0.5},
    {"field": "suburb",    "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.85, "label": "suburb",    "weight": 0.5},
    {"field": "state",     "method": "exact", "label": "state",     "weight": 0.5},
    {"field": "address_2", "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_2", "weight": 0.5},
]

# Classification configuration
CLASSIFICATION_THRESHOLD = 4

# Clustering configuration
CLUSTERING_THRESHOLD = 8