# --- File: config.py ---

# File configuration
INPUT_FILE = "dedup_data.csv"
RESULTS_FILE = "found_duplicate_pairs.csv"

# --- Indexing Configuration ---
SORTING_WINDOW_SIZE = 11

# Comparison fields and methods
# We can now use a simple list, as preprocessing solved
# the swapped-name problem. We compare name_1->name_1 and name_2->name_2.
COMPARISON_FIELDS = [
    # Use our new canonical name fields
    {"field": "name_1",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "name_1"},
    {"field": "name_2",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85, "label": "name_2"},
    
    # Address fields remain the same
    {"field": "address_1", "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80, "label": "address_1"},
    {"field": "suburb",    "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.85, "label": "suburb"},
    {"field": "state",     "method": "exact", "label": "state"}
]

# Classification configuration
# We are back to a simple sum.
# Max score is 5.0. Start tuning from a mid-point.
CLASSIFICATION_THRESHOLD = 3