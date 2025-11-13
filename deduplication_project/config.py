# --- File: config.py ---

# File configuration
INPUT_FILE = "dedup_data.csv"
RESULTS_FILE = "found_duplicate_pairs.csv"

# --- Indexing Configuration ---
SORTING_WINDOW_SIZE = 15
POSTCODE_SORTING_WINDOW_SIZE = 5
ADDRESS_SORTING_WINDOW_SIZE = 5  # <-- NEW (for our 5th pass)

# Comparison fields and methods
# (TUNED) Weights re-balanced. Total score is 16.0
COMPARISON_FIELDS = [
    # --- Name Fields (Weight: 1.5 each = 3.0 total) ---
    # (TUNED) Lowered weight from 2.0 to 1.5
    {"field": "given_name", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "given_name", "weight": 1.5},
    {"field": "surname",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "surname", "weight": 1.5},
    
    # Crossed-field comparisons (Weight: 1.5 each)
    {"field_left": "given_name", "field_right": "surname", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "gv_vs_sn", "weight": 1.5},
     
    {"field_left": "surname", "field_right": "given_name", 
     "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "sn_vs_gv", "weight": 1.5},

    # --- Detail Fields (Weight: 3.5 each = 7.0 total) ---
    # (TUNED) Increased weight from 3.0 to 3.5
    {"field": "soc_sec_id",    "method": "string", "string_method": "jarowinkler", "threshold": 0.90, "label": "soc_sec_id", "weight": 3.5},
    {"field": "date_of_birth", "method": "string", "string_method": "jarowinkler", "threshold": 0.90, "label": "date_of_birth", "weight": 3.5},

    # --- Address Fields (Weight: 0.5 - 1.5 each = 6.0 total) ---
    # (TUNED) Increased weight of address fields
    {"field": "address_1", "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_1", "weight": 1.5}, # <-- Tuned
    {"field": "postcode",  "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "postcode",  "weight": 1.5}, # <-- Tun.
    {"field":"street_number", "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "street_number", "weight": 1.0},
    {"field": "suburb",    "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.85, "label": "suburb",    "weight": 1.0},
    {"field": "state",     "method": "exact", "label": "state",     "weight": 0.25},
    {"field": "address_2", "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_2", "weight": 0.25},
]

# Classification configuration
# Max score is 16.0. Let's start with your best threshold.
CLASSIFICATION_THRESHOLD = 7.5

# Clustering configuration
CLUSTERING_THRESHOLD = 12.0