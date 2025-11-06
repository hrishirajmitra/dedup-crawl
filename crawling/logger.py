# logger.py
"""
Initializes a standard, clean logger for the project.
"""

import logging
import sys

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout  # Log to standard output
)

# Get the logger instance
logger = logging.getLogger(__name__)