# Text Formatter Microservice

A simple microservice that converts text to different cases or removes special characters.

## Author
Elizabeth

## Features
- Convert text to **uppercase**
- Convert text to **lowercase**
- Convert text to **title case**
- **Clean** text by removing special characters (keeps letters, numbers, spaces)

## Communication
Uses text files for inter-process communication.

- **Request file:** `text_formatter_request.txt`
- **Response file:** `text_formatter_response.txt`

## How to Run
```bash
python text_formatter.py
```
The service will continuously monitor for requests until stopped with Ctrl+C.

## Request Format
Write a JSON object to `text_formatter_request.txt`:

```json
{
    "text": "your text here",
    "format": "upper"
}
```

### Format Options
| Option | Description | Example Input | Example Output |
|--------|-------------|---------------|----------------|
| `upper` | Convert to uppercase | "hello world" | "HELLO WORLD" |
| `lower` | Convert to lowercase | "HELLO WORLD" | "hello world" |
| `title` | Convert to title case | "hello world" | "Hello World" |
| `clean` | Remove special characters | "Hello! #test" | "Hello test" |

## Response Format
The service writes a JSON response to `text_formatter_response.txt`:

### Success Response
```json
{
    "success": true,
    "result": "FORMATTED TEXT",
    "error": ""
}
```

### Error Response
```json
{
    "success": false,
    "result": "",
    "error": "Error description"
}
```

## Example Usage (Python)

```python
import json
import time
from pathlib import Path

def format_text_via_service(text, format_type):
    """Send a request to the Text Formatter microservice."""
    request_file = Path("text_formatter_request.txt")
    response_file = Path("text_formatter_response.txt")
    
    # Clear response file
    response_file.write_text("")
    
    # Write request
    request = {"text": text, "format": format_type}
    request_file.write_text(json.dumps(request))
    
    # Wait for response
    while True:
        time.sleep(0.1)
        content = response_file.read_text().strip()
        if content:
            return json.loads(content)

# Example
result = format_text_via_service("hello world", "upper")
print(result["result"])  # Output: HELLO WORLD
```

## Error Handling
- Empty text inputs are handled gracefully (returns empty string)
- Invalid format types return an error message
- Invalid JSON in request file returns an error message
