"""
Text Formatter Microservice
Author: Elizabeth

Converts text to uppercase/lowercase/title case, or removes special characters.

Communication: Text files
- Request file: text_formatter_request.txt
- Response file: text_formatter_response.txt

Request format (JSON):
{
    "text": "string to format",
    "format": "upper" | "lower" | "title" | "clean"
}

Response format (JSON):
{
    "success": true/false,
    "result": "formatted string",
    "error": "error message if any"
}
"""

import json
import time
import re
from pathlib import Path

REQUEST_FILE = "text_formatter_request.txt"
RESPONSE_FILE = "text_formatter_response.txt"
POLL_INTERVAL = 0.1  # seconds


def format_text(text: str, format_type: str) -> str:
    """Apply the specified formatting to the text."""
    if format_type == "upper":
        return text.upper()
    elif format_type == "lower":
        return text.lower()
    elif format_type == "title":
        return text.title()
    elif format_type == "clean":
        # Remove special characters, keep letters, numbers, and spaces
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)
    else:
        raise ValueError(f"Unknown format type: {format_type}")


def process_request(request_data: dict) -> dict:
    """Process a formatting request and return the response."""
    try:
        text = request_data.get("text", "")
        format_type = request_data.get("format", "").lower()
        
        if not format_type:
            return {
                "success": False,
                "result": "",
                "error": "Missing 'format' field. Use 'upper', 'lower', 'title', or 'clean'."
            }
        
        if format_type not in ["upper", "lower", "title", "clean"]:
            return {
                "success": False,
                "result": "",
                "error": f"Invalid format type '{format_type}'. Use 'upper', 'lower', 'title', or 'clean'."
            }
        
        # Handle empty or None text gracefully
        if text is None:
            text = ""
        
        result = format_text(str(text), format_type)
        
        return {
            "success": True,
            "result": result,
            "error": ""
        }
        
    except Exception as e:
        return {
            "success": False,
            "result": "",
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
        return {"error": "Invalid JSON in request file"}
    except Exception:
        return None


def write_response(response: dict):
    """Write the response to the response file."""
    response_path = Path(RESPONSE_FILE)
    response_path.write_text(json.dumps(response, indent=2))


def main():
    """Main loop - continuously monitor for requests."""
    print("=" * 50)
    print("Text Formatter Microservice")
    print("=" * 50)
    print(f"Monitoring: {REQUEST_FILE}")
    print(f"Responses:  {RESPONSE_FILE}")
    print(f"Commands:   upper, lower, title, clean")
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
                if "error" in request and len(request) == 1:
                    # JSON parse error
                    response = {
                        "success": False,
                        "result": "",
                        "error": request["error"]
                    }
                else:
                    print(f"Received request: {request}")
                    response = process_request(request)
                    print(f"Sending response: {response}")
                    print()
                
                write_response(response)
            
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            print("\nShutting down Text Formatter Microservice...")
            break


if __name__ == "__main__":
    main()
