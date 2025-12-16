# Book Library Database Manager

A beautiful, interactive command-line application for managing your book collection with Rich-formatted tables and menus.

## Features

- **Interactive Visual CLI** - Beautiful menus, tables, and colored output using Rich
- **Book Management** - Add, list, and manage books with title, author, ISBN, and publication year
- **Pagination** - Navigate through large collections with keyboard controls
- **ISBN Validation** - Toggle ISBN-10 and ISBN-13 format validation
- **Auto-sorting** - Database automatically maintains chronological order by publication year
- **Data Validation** - Invalid entries are detected and reported with detailed warnings

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

### macOS / Linux

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Windows

1. **Create a virtual environment:**
   ```cmd
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   ```cmd
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

## Usage

### Starting the Application

**With a specific database file:**
```bash
python book_library.py library.txt
```

**Without arguments (will prompt for filename):**
```bash
python book_library.py
```

### Interactive Menu

Once started, you'll see a beautiful interactive menu with the following options:

1. **Add Book** - Add a new book to your collection
   - Enter title, author, ISBN, and publication year
   - Optional ISBN validation ensures proper format

2. **List Books** - View all books in a formatted table
   - Books are displayed sorted by publication year
   - Navigate pages using keyboard:
     - `n` - Next page
     - `p` - Previous page
     - Enter page number to jump directly
     - `q` - Return to main menu

3. **Toggle Validation** - Enable/disable ISBN format validation
   - When enabled, validates ISBN-10 and ISBN-13 formats

4. **Exit** - Close the application

### Database File Format

The database file stores books in plain text format:
```
Title/Author/ISBN/Year
```

Example:
```
1984/George Orwell/978-0451524935/1949
The Great Gatsby/F. Scott Fitzgerald/978-0743273565/1925
```

**Important:**
- The file is automatically kept sorted by publication year
- Invalid entries are detected on startup and removed
- All modifications are immediately saved to the file

## How It Works

### Data Storage
- Books are stored in a plain text file with `/` as delimiter
- Each line contains: `Title/Author/ISBN/Year`
- File is automatically sorted by year on every load and save

### Loading Process
1. File is read and parsed line by line
2. Invalid entries (wrong format, invalid year) are tracked
3. Valid books are loaded into memory
4. File is re-saved in sorted order
5. Warnings are displayed if any entries were invalid

### Adding Books
1. User enters book details via interactive prompts
2. Input validation ensures all fields are provided
3. Year must be a valid integer
4. If ISBN validation is enabled, ISBN format is checked
5. Book is added to collection and file is saved in sorted order

### Pagination
- Lists display 10 books per page by default
- Total pages calculated based on book count
- Navigation allows moving between pages or jumping directly to a specific page

## Example Session

```bash
# Start with test library
python book_library.py test_library.txt

# The application shows:
# - Welcome screen
# - Database file confirmation
# - Any warnings about invalid entries
# - Interactive menu

# Select option 2 to list books
# Use 'n' and 'p' to navigate through pages
# Press 'q' to return to menu

# Select option 1 to add a new book
# Follow the prompts to enter book details

# Select option 4 to exit
```

## Deactivating Virtual Environment

When you're done using the application:

**macOS / Linux:**
```bash
deactivate
```

**Windows:**
```cmd
deactivate
```

## Test Data

A test database file `test_library.txt` with 60 classic books is included for testing pagination and browsing features.

## Troubleshooting

**"Module not found" error:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**Invalid entries warning:**
- Check the database file for lines with incorrect format
- Ensure each line has exactly 4 fields separated by `/`
- Year field must be a valid integer

**File not found:**
- Create a new empty file with the specified name, or
- Let the program create it automatically when you add your first book
