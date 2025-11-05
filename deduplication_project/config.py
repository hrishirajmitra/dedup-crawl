# --- File: config.py ---

# File configuration
INPUT_FILE = "dedup_data.csv"
RESULTS_FILE = "found_duplicate_pairs.csv"

# --- Indexing Configuration ---
SORTING_WINDOW_SIZE = 15

# --- File: config.py ---

# ... (other config is the same) ...

# Comparison fields and methods
# This is the advanced list for handling swapped names AND all new fields.
COMPARISON_FIELDS = [
    # --- Name Fields (for 'name_score') ---
    {"field": "given_name", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "given_name"},
    {"field": "surname",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "surname"},
    
    # Crossed-field comparisons
    {"field_left": "given_name", "field_right": "surname", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "gv_vs_sn"},
     
    {"field_left": "surname", "field_right": "given_name", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "sn_vs_gv"},

    # --- Address Fields (for 'address_score') ---
    {"field": "street_number", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "street_number"},
    {"field": "address_1",  "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_1"},
    {"field": "address_2",  "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_2"},
    {"field": "suburb",     "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.85, "label": "suburb"},
    {"field": "postcode",   "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "postcode"},
    {"field": "state",      "method": "exact", "label": "state"},
    
    # --- Detail Fields (for 'detail_score') ---
    {"field": "date_of_birth", "method": "string", "string_method": "jarowinkler", "threshold": 0.90, "label": "date_of_birth"},
    {"field": "soc_sec_id",    "method": "string", "string_method": "jarowinkler", "threshold": 0.90, "label": "soc_sec_id"}
]

# Classification configuration
# The max score is now 11 (2 for name + 6 for address + 3 for details).
# We'll need to tune this threshold again. Let's start high.
CLASSIFICATION_THRESHOLD = 5