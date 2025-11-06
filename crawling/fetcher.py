# fetcher.py
"""
Handles fetching and parsing page data from the web server.
This version parses HTML.
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional, Dict, List, Any
from config import BASE_URL, REQUEST_TIMEOUT
from logger import logger

def find_start_page_id() -> Optional[str]:
    """
    Fetches the base URL (/) to discover the initial start page ID.
    """
    logger.info(f"Discovering start page ID from {BASE_URL}/")
    try:
        response = requests.get(BASE_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        if 'text/html' not in response.headers.get('Content-Type', ''):
            logger.error("Server did not return HTML from root URL.")
            return None

        soup = BeautifulSoup(response.text, 'lxml')
        
        # 1. Extract Page ID from the root page
        page_id_tag = soup.find('div', class_='page-id')
        if not page_id_tag:
            logger.error("Could not find 'page-id' tag on root page.")
            return None
            
        extracted_page_id = page_id_tag.text.split(':')[-1].strip()
        logger.info(f"Discovered start page ID: {extracted_page_id}")
        return extracted_page_id

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error finding start page: {e}")
    except requests.exceptions.ConnectionError:
        logger.error("Connection error finding start page. Server may be down.")
    except Exception as e:
        logger.error(f"An unexpected error occurred while finding start page: {e}")
    
    return None

def _parse_node_history(details_tag) -> List[Dict[str, str]]:
    """Helper function to parse the node history <details> tag."""
    # ... (This function remains unchanged)
    history = []
    if not details_tag:
        return history
    
    try:
        # Find all 'div' items representing past nodes
        history_items = details_tag.find_all('div', recursive=False)[-1].find_all('div')
        for item in history_items:
            text = item.text.strip('• ')
            if '(' in text and ')' in text:
                parts = text.split(' (', 1)
                node_id = parts[0]
                timestamp = parts[1].strip(')')
                history.append({"node_id": node_id, "timestamp": timestamp})
    except Exception as e:
        logger.warning(f"Could not parse node history: {e}")
    return history

def fetch_page(page_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetches a single page from the server, parses its HTML,
    and returns its content as a dictionary.
    """
    # ... (This function remains unchanged)
    url = f"{BASE_URL}/{page_id}"
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        
        if 'text/html' not in response.headers.get('Content-Type', ''):
            logger.error(f"Server returned non-HTML content for page {page_id}.")
            return None

        # --- Parse the HTML ---
        soup = BeautifulSoup(response.text, 'lxml')
        
        # 1. Extract Page ID
        page_id_tag = soup.find('div', class_='page-id')
        extracted_page_id = page_id_tag.text.split(':')[-1].strip()

        # 2. Extract Node ID
        node_id_tag = soup.find('span', class_='node-id')
        extracted_node_id = node_id_tag.find('b').text.strip()
        
        # 3. Extract Node History
        details_tag = soup.find('details')
        extracted_history = _parse_node_history(details_tag)
        
        # 4. Extract Outgoing Links
        links = []
        table = soup.find('table', class_='files-table')
        if table:
            for link_tag in table.find_all('a', class_='file-link'):
                href = link_tag.get('href', '')
                link_page_id = href.split('/')[-1]
                if link_page_id:
                    links.append(link_page_id)

        # --- Build the same dictionary structure as before ---
        return {
            "page_id": extracted_page_id,
            "node_id": extracted_node_id,
            "node_history": extracted_history,
            "outgoing_links": links
        }

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for page {page_id}: {e}")
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for page {page_id}. Server may be down.")
    except requests.exceptions.Timeout:
        logger.error(f"Request timeout for page {page_id}")
    except AttributeError as e:
        logger.error(f"Failed to parse HTML for page {page_id}. Structure may be new. Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred for page {page_id}: {e}")
    
    return None