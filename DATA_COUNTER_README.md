# Data Counter Microservice

A microservice that counts items in lists or provides text statistics.

## Author
Elizabeth

## Features
- **Count Mode:** Count total items, unique items, and frequency of each item in a list
- **Stats Mode:** Get character count and word count for text

## Communication
Uses text files for inter-process communication.

- **Request file:** `data_counter_request.txt`
- **Response file:** `data_counter_response.txt`

## How to Run
```bash
python data_counter.py
```
The service will continuously monitor for requests until stopped with Ctrl+C.

## Request Format
Write a JSON object to `data_counter_request.txt`:

### Count Mode (for lists)
```json
{
    "mode": "count",
    "data": ["item1", "item2", "item1", "item3"]
}
```

### Stats Mode (for text)
```json
{
    "mode": "stats",
    "data": "Your text string here"
}
```

## Response Format

### Count Mode Response
```json
{
    "success": true,
    "total_count": 4,
    "unique_count": 3,
    "item_counts": {
        "item1": 2,
        "item2": 1,
        "item3": 1
    },
    "error": ""
}
```

### Stats Mode Response
```json
{
    "success": true,
    "character_count": 21,
    "word_count": 4,
    "error": ""
}
```

### Error Response
```json
{
    "success": false,
    "error": "Error description"
}
```

## Example Usage (Python)

```python
import json
import time
from pathlib import Path


def count_items_via_service(items):
    """Send a count request to the Data Counter microservice."""
    request_file = Path("../../bookbase/data_counter_request.txt")
    response_file = Path("../../bookbase/data_counter_response.txt")

    # Clear response file
    response_file.write_text("")

    # Write request
    request = {"mode": "count", "data": items}
    request_file.write_text(json.dumps(request))

    # Wait for response
    while True:
        time.sleep(0.1)
        content = response_file.read_text().strip()
        if content:
            return json.loads(content)


def get_text_stats_via_service(text):
    """Send a stats request to the Data Counter microservice."""
    request_file = Path("../../bookbase/data_counter_request.txt")
    response_file = Path("../../bookbase/data_counter_response.txt")

    # Clear response file
    response_file.write_text("")

    # Write request
    request = {"mode": "stats", "data": text}
    request_file.write_text(json.dumps(request))

    # Wait for response
    while True:
        time.sleep(0.1)
        content = response_file.read_text().strip()
        if content:
            return json.loads(content)


# Example: Count genres
genres = ["Fantasy", "Fantasy", "Romance", "Sci-Fi", "Fantasy"]
result = count_items_via_service(genres)
print(f"Total: {result['total_count']}, Unique: {result['unique_count']}")
print(f"Breakdown: {result['item_counts']}")

# Example: Text stats
result = get_text_stats_via_service("Hello world, this is a test.")
print(f"Characters: {result['character_count']}, Words: {result['word_count']}")
```

## Use Cases
- Count genres in a book list
- Count authors in a reading list
- Get statistics on book descriptions or notes
- Count unique tags or categories

## Error Handling
- Empty lists return counts of 0
- Empty text returns character_count: 0, word_count: 0
- Invalid mode returns an error message
- Invalid JSON in request file returns an error message
