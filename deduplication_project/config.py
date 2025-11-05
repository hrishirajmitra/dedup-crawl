# --- File: config.py ---

# File configuration
INPUT_FILE = "dedup_data.csv"
RESULTS_FILE = "found_duplicate_pairs.csv"

# Indexing (Blocking) configuration
# 'postcode' is a good choice as it's reliable and splits the data well.
# Using the first 3 chars of 'surname' is also a good alternative.
BLOCK_ON_FIELD = "postcode"

# Comparison fields and methods
# We define which fields to compare and what logic to use.
# 'method' can be 'string', 'exact', 'numeric', etc.
# 'threshold' is for string comparisons (0.0 to 1.0)
# --- File: config.py ---
...

COMPARISON_FIELDS = [
    {"field": "given_name", "method": "string", "string_method": "jarowinkler", "threshold": 0.85},
    {"field": "surname",    "method": "string", "string_method": "jarowinkler", "threshold": 0.85},
    {"field": "address_1",  "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.80},
    {"field": "suburb",     "method": "string", "string_method": "damerau_levenshtein", "threshold": 0.85},
    {"field": "state",      "method": "exact"}
]
...

# Classification configuration
# This is the minimum *sum* of similarity scores for a pair to be
# considered a duplicate.
# Max score = 5 (1.0 for each of the 5 fields).
# A threshold of 4.0 means we allow for some typos in one or two fields.
CLASSIFICATION_THRESHOLD = 2