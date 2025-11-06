# config.py
"""
Configuration file for the crawler pipeline.
"""

# Server configuration
BASE_URL = "http://localhost:3000"
REQUEST_TIMEOUT = 5  # 5-second timeout for requests

# PageRank algorithm parameters
DAMPING_FACTOR = 0.85  # Standard damping factor
MAX_ITERATIONS = 100   # Max iterations for convergence
TOLERANCE = 1.0e-6     # Convergence tolerance