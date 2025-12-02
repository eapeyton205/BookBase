# BookBase - Reading List Manager

A smart web application for managing your to-be-read (TBR) list with intelligent series tracking and personalized book suggestions.

## Features

- **Book Management** - Add books to your reading list with details like title, author, genre, and series information
- **Series Tracking** - Automatically tracks book series and their reading order
- **Smart Suggestions** - Get random book recommendations that respect series order (no spoilers!)
- **Reading History** - Keep track of books you've completed
- **Statistics** - View breakdowns of your reading by genre and author
- **Easy Editing** - Update book details or fix mistakes anytime
- **Flexible Workflow** - Mark books as read/unread as needed

## Microservices Architecture

BookBase uses four microservices that communicate via text files:

| Microservice | Type | Description |
|--------------|------|-------------|
| **RNG Service** | Small Pool | Random book selection for suggestions |
| **Text Formatter** | Big Pool | Formats book titles to proper title case |
| **Data Counter** | Big Pool | Counts books by genre and author for statistics |
| **Words Service** | Big Pool | Analyzes common words in book titles |

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone this repository:
```bash
git clone https://github.com/eapeyton205/bookbase.git
cd bookbase
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start each microservice in a separate terminal:

```bash
# Terminal 1
python rng_service.py

# Terminal 2
python text_formatter.py

# Terminal 3
python data_counter.py

# Terminal 4
python words_service.py

# Terminal 5
streamlit run bookbase.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### Adding Books
1. Navigate to the "Add Book" tab
2. Enter the book title and author (required)
3. Optionally add genre and series information
4. Click "Add Book to TBR"

### Getting Suggestions
1. Go to the "Get Suggestion" tab
2. Click "Get Random Suggestion" to receive a recommendation
3. The app will only suggest books you're ready to read based on series order

### Managing Your List
- **View all books**: Check the "My TBR List" tab to see your books organized by series
- **Edit books**: Click the edit icon to update book details
- **Mark as read**: Click the checkmark icon to move books to your reading history
- **Remove books**: Click the trash icon to delete books from your list

### Reading History
- View completed books in the "Reading History" tab
- Click "Unread" to move a book back to your TBR list

### Statistics
- View genre and author breakdowns in the "Statistics" tab
- Analyze common words in your book titles

## How It Works

BookBase uses smart series tracking to ensure you never get spoilers:
- Books are organized by series automatically
- Suggestions only include books where you've read all previous books in the series
- Standalone books are always available for suggestions

## Data Storage

Your reading data is stored locally in JSON files:
- `books.json` - Your TBR list
- `read_books.json` - Your reading history

These files are automatically created when you first use the app.

## Technology Stack

- **Streamlit** - Web application framework
- **Python** - Core programming language
- **JSON** - Local data storage

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

Elizabeth Peyton

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- RNG Service co-written with Lenin Soto-Hernandez
- Words Service by Silas Jones