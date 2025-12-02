"""
Data Counter Microservice
Author: Elizabeth Peyton

Counts items in a list (total and unique) or provides character/word statistics.

Communication: Text files
- Request file: data_counter_request.txt
- Response file: data_counter_response.txt

Request format (JSON):
{
    "mode": "count" | "stats",
    "data": ["item1", "item2", ...] for count mode, or "text string" for stats mode
}

Response format (JSON):

For "count" mode:
{
    "success": true/false,
    "total_count": number,
    "unique_count": number,
    "item_counts": {"item": count, ...},
    "error": ""
}

For "stats" mode:
{
    "success": true/false,
    "character_count": number,
    "word_count": number,
    "error": ""
}
"""

import json
import time
from pathlib import Path
from collections import Counter

REQUEST_FILE = "data_counter_request.txt"
RESPONSE_FILE = "data_counter_response.txt"
POLL_INTERVAL = 0.1  # seconds


def count_items(items: list) -> dict:
    """Count total items, unique items, and frequency of each item."""
    if not isinstance(items, list):
        raise ValueError("Data must be a list of items")
    
    # Convert all items to strings for consistent counting
    str_items = [str(item) for item in items]
    
    item_counts = dict(Counter(str_items))
    
    return {
        "success": True,
        "total_count": len(str_items),
        "unique_count": len(item_counts),
        "item_counts": item_counts,
        "error": ""
    }


def get_text_stats(text: str) -> dict:
    """Get character count and word count for text."""
    if text is None:
        text = ""
    
    text = str(text)
    
    char_count = len(text)
    
    # Count words (split by whitespace)
    words = text.split()
    word_count = len(words)
    
    return {
        "success": True,
        "character_count": char_count,
        "word_count": word_count,
        "error": ""
    }


def process_request(request_data: dict) -> dict:
    """Process a counting request and return the response."""
    try:
        mode = request_data.get("mode", "").lower()
        data = request_data.get("data")
        
        if not mode:
            return {
                "success": False,
                "error": "Missing 'mode' field. Use 'count' or 'stats'."
            }
        
        if mode == "count":
            if data is None:
                return {
                    "success": False,
                    "error": "Missing 'data' field. Provide a list of items."
                }
            if not isinstance(data, list):
                return {
                    "success": False,
                    "error": "'data' must be a list of items for 'count' mode."
                }
            return count_items(data)
            
        elif mode == "stats":
            if data is None:
                data = ""
            return get_text_stats(data)
            
        else:
            return {
                "success": False,
                "error": f"Invalid mode '{mode}'. Use 'count' or 'stats'."
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def read_request() -> dict | None:
    """Read and parse the request file if it exists and has content."""
    request_path = Path(REQUEST_FILE)
    
    if not request_path.exists():
        return None
    
    try:
        content = request_path.read_text().strip()
        if not content:
            return None
        
        # Parse JSON request
        request_data = json.loads(content)
        
        # Clear the request file after reading
        request_path.write_text("")
        
        return request_data
        
    except json.JSONDecodeError:
        # Clear invalid request
        request_path.write_text("")
        return {"_parse_error": "Invalid JSON in request file"}
    except Exception:
        return None


def write_response(response: dict):
    """Write the response to the response file."""
    response_path = Path(RESPONSE_FILE)
    response_path.write_text(json.dumps(response, indent=2))


def main():
    """Main loop - continuously monitor for requests."""
    print("=" * 50)
    print("Data Counter Microservice")
    print("=" * 50)
    print(f"Monitoring: {REQUEST_FILE}")
    print(f"Responses:  {RESPONSE_FILE}")
    print(f"Modes:      count, stats")
    print("=" * 50)
    print("Waiting for requests... (Ctrl+C to stop)")
    print()
    
    # Initialize files
    Path(REQUEST_FILE).touch()
    Path(RESPONSE_FILE).write_text("")
    
    while True:
        try:
            request = read_request()
            
            if request:
                if "_parse_error" in request:
                    response = {
                        "success": False,
                        "error": request["_parse_error"]
                    }
                else:
                    print(f"Received request: {request}")
                    response = process_request(request)
                    print(f"Sending response: {response}")
                    print()
                
                write_response(response)
            
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nShutting down Data Counter Microservice...")
            break


if __name__ == "__main__":
    main()
