# --- File: config.py ---

import yaml
from pathlib import Path

# Load configuration from YAML file
CONFIG_FILE = Path(__file__).parent / "config.yaml"

with open(CONFIG_FILE, 'r') as f:
    _config = yaml.safe_load(f)

# File configuration
INPUT_FILE = _config['files']['input']
RESULTS_FILE = _config['files']['results']

# Indexing configuration
SORTING_WINDOW_SIZE = _config['indexing']['sorting_window_size']

# Classification configuration
CLASSIFICATION_THRESHOLD = _config['classification']['threshold']

# Comparison fields
COMPARISON_FIELDS = _config['comparison_fields']
CLUSTERING_THRESHOLD =  _config['clustering']['threshold']