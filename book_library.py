#!/usr/bin/env python3
"""Library Database Program - Manages book collection with file storage."""

import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich import box

console = Console()


class Book:
    """Represents a book with title, author, ISBN, and year."""

    def __init__(self, title, author, isbn, year):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = int(year)

    def to_file_format(self):
        """Convert book to file storage format."""
        return f"{self.title}/{self.author}/{self.isbn}/{self.year}"

    def __repr__(self):
        return f"Book({self.title}, {self.author}, {self.year})"


class LibraryDatabase:
    """Manages library database with file persistence."""

    def __init__(self, filename):
        self.filename = filename
        self.books = []
        self.validate_isbn = False
        self.load_warnings = []
        self._load_from_file()

    def _load_from_file(self):
        """Load books from file and ensure sorted order."""
        invalid_entries = []
        try:
            with open(self.filename, "r") as f:
                for line_num, line in enumerate(f, start=1):
                    if line.strip():
                        parts = line.strip().split("/")
                        if len(parts) == 4:
                            try:
                                book = Book(parts[0], parts[1], parts[2], parts[3])
                                self.books.append(book)
                            except (ValueError, Exception) as e:
                                invalid_entries.append((line_num, line.strip(), str(e)))
                        else:
                            invalid_entries.append((line_num, line.strip(), "Invalid format (expected 4 fields)"))

            # Store warnings for later display
            self.load_warnings = invalid_entries

            # Reorder file after loading to ensure it stays sorted
            if self.books:
                self._save_to_file()
        except FileNotFoundError:
            pass  # Starting fresh

    def _save_to_file(self):
        """Save books to file sorted by year."""
        sorted_books = sorted(self.books, key=lambda b: b.year)
        with open(self.filename, "w") as f:
            for book in sorted_books:
                f.write(book.to_file_format() + "\n")

    def _validate_isbn_format(self, isbn):
        """Validate ISBN format (ISBN-10 or ISBN-13)."""
        # Remove hyphens and spaces
        isbn_clean = isbn.replace("-", "").replace(" ", "")

        # Check ISBN-10 format (10 digits, last can be X)
        if len(isbn_clean) == 10:
            if isbn_clean[:-1].isdigit() and (
                isbn_clean[-1].isdigit() or isbn_clean[-1].upper() == "X"
            ):
                return True, "ISBN-10"

        # Check ISBN-13 format (13 digits, starts with 978 or 979)
        if len(isbn_clean) == 13:
            if isbn_clean.isdigit() and (
                isbn_clean.startswith("978") or isbn_clean.startswith("979")
            ):
                return True, "ISBN-13"

        return False, None

    def add(self, title, author, isbn, year):
        """Add a new book to the database."""
        # Validate inputs
        if not title or not author or not isbn or not year:
            console.print("[red]Error: All fields are required[/red]")
            return

        try:
            year_int = int(year)
        except ValueError:
            console.print("[red]Error: Year must be a valid number[/red]")
            return

        # Validate ISBN if enabled
        if self.validate_isbn:
            is_valid, isbn_type = self._validate_isbn_format(isbn)
            if not is_valid:
                console.print("[red]Error: Invalid ISBN format (must be ISBN-10 or ISBN-13)[/red]")
                return
            console.print(f"[green]✓ Valid {isbn_type} format[/green]")

        # Add book
        new_book = Book(title, author, isbn, year_int)
        self.books.append(new_book)
        self._save_to_file()
        console.print(f"[green]✓ Book added successfully: {title} by {author} ({year_int})[/green]")

    def list(self, page=1, page_size=10):
        """List all books in the database, sorted by year with pagination."""
        if not self.books:
            console.print("[yellow]⚠ No books in database[/yellow]")
            return False

        sorted_books = sorted(self.books, key=lambda b: b.year)
        total_books = len(sorted_books)
        total_pages = (total_books + page_size - 1) // page_size

        # Ensure page is within bounds
        page = max(1, min(page, total_pages))

        # Calculate slice indices
        start_idx = (page - 1) * page_size
        end_idx = min(start_idx + page_size, total_books)
        page_books = sorted_books[start_idx:end_idx]

        # Create a Rich table
        table = Table(
            title=f"📚 Library Database - {total_books} book(s) | Page {page}/{total_pages}",
            show_header=True,
            header_style="bold cyan"
        )
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("Title", style="magenta", width=40)
        table.add_column("Author", style="green", width=30)
        table.add_column("ISBN", style="yellow", width=20)
        table.add_column("Year", style="cyan", width=6, justify="right")

        for i, book in enumerate(page_books, start=start_idx + 1):
            title = book.title[:40] if len(book.title) > 40 else book.title
            author = book.author[:30] if len(book.author) > 30 else book.author
            isbn = book.isbn[:20] if len(book.isbn) > 20 else book.isbn
            table.add_row(str(i), title, author, isbn, str(book.year))

        console.print(table)

        # Show navigation hints
        if total_pages > 1:
            console.print("\n[dim]Navigation: (n)ext | (p)revious | (number) go to page | (q)uit[/dim]")

        return total_pages > 1

    def toggle_validation(self):
        """Toggle ISBN validation on/off."""
        self.validate_isbn = not self.validate_isbn
        status = "enabled" if self.validate_isbn else "disabled"
        color = "green" if self.validate_isbn else "yellow"
        console.print(f"[{color}]ISBN validation is now {status}[/{color}]")


def show_menu(db):
    """Display the main menu."""
    console.clear()

    # Create header
    header = Panel(
        "[bold cyan]📚 Library Database Manager[/bold cyan]\n"
        f"[dim]Database: {db.filename}[/dim]\n"
        f"[dim]Books: {len(db.books)} | ISBN Validation: {'[green]ON[/green]' if db.validate_isbn else '[yellow]OFF[/yellow]'}[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    )
    console.print(header)
    console.print()

    # Create menu table with clean styling
    menu_table = Table(
        show_header=True,
        header_style="bold magenta",
        box=None,
        padding=(0, 2)
    )

    menu_table.add_column("Option", style="bold cyan", width=8, justify="center")
    menu_table.add_column("Action", style="bold white", width=25)
    menu_table.add_column("Description", style="dim white", width=40)

    menu_table.add_row(
        "[bold cyan]1[/bold cyan]",
        "Add Book",
        "Add a new book to your collection"
    )
    menu_table.add_row(
        "[bold cyan]2[/bold cyan]",
        "List Books",
        "View all books in your library"
    )
    menu_table.add_row(
        "[bold cyan]3[/bold cyan]",
        "Toggle Validation",
        f"Currently: {'[green]Enabled[/green]' if db.validate_isbn else '[yellow]Disabled[/yellow]'}"
    )
    menu_table.add_row(
        "[bold cyan]4[/bold cyan]",
        "Exit",
        "Close the application"
    )

    console.print(menu_table)
    console.print()


def add_book_interactive(db):
    """Interactively add a book."""
    console.print("\n[bold cyan]➕ Add New Book[/bold cyan]\n")

    title = Prompt.ask("[yellow]Book title[/yellow]")
    if not title:
        console.print("[red]✗ Title cannot be empty[/red]")
        return

    author = Prompt.ask("[yellow]Author[/yellow]")
    if not author:
        console.print("[red]✗ Author cannot be empty[/red]")
        return

    isbn = Prompt.ask("[yellow]ISBN[/yellow]")
    if not isbn:
        console.print("[red]✗ ISBN cannot be empty[/red]")
        return

    year = Prompt.ask("[yellow]Publication year[/yellow]")
    if not year:
        console.print("[red]✗ Year cannot be empty[/red]")
        return

    db.add(title, author, isbn, year)


def main():
    """Entry point with interactive CLI."""
    console.clear()

    # Welcome banner
    welcome = Panel(
        "[bold cyan]Welcome to Library Database Manager![/bold cyan]\n"
        "[dim]Manage your book collection with style[/dim]",
        box=box.DOUBLE,
        border_style="cyan"
    )
    console.print(welcome)
    console.print()

    # Get database filename from command-line argument or prompt
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        console.print(f"[dim]Using database file: {filename}[/dim]\n")
    else:
        filename = Prompt.ask(
            "[yellow]Enter database filename[/yellow]",
            default="library.txt"
        )

    # Create database instance
    db = LibraryDatabase(filename)

    # Show warnings if any invalid entries were found
    if db.load_warnings:
        console.print("\n[bold yellow]⚠ Warning: Invalid entries found and removed:[/bold yellow]")
        for line_num, line, reason in db.load_warnings:
            console.print(f"[yellow]  Line {line_num}: {line[:60]}... - {reason}[/yellow]")
        console.print("\n[dim]Press Enter to continue...[/dim]")
        input()

    # Main loop
    while True:
        show_menu(db)

        choice = Prompt.ask(
            "[bold green]Select an option[/bold green]",
            choices=["1", "2", "3", "4"],
            default="2"
        )

        if choice == "1":
            add_book_interactive(db)
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
        elif choice == "2":
            console.print()
            page = 1
            while True:
                has_pagination = db.list(page=page, page_size=10)
                if not has_pagination:
                    console.print("\n[dim]Press Enter to continue...[/dim]")
                    input()
                    break

                nav = Prompt.ask("\n[bold cyan]Navigation[/bold cyan]", default="q").lower()
                if nav == "n":
                    page += 1
                elif nav == "p":
                    page = max(1, page - 1)
                elif nav == "q":
                    break
                elif nav.isdigit():
                    page = int(nav)
                console.print()
        elif choice == "3":
            db.toggle_validation()
            console.print("\n[dim]Press Enter to continue...[/dim]")
            input()
        elif choice == "4":
            console.print("\n[bold cyan]👋 Goodbye! Thanks for using Library Database Manager.[/bold cyan]\n")
            break


if __name__ == "__main__":
    main()
