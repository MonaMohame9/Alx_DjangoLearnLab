from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
author = Author.objects.get(name="George Orwell")
books_by_author = Book.objects.filter(author=author)
print("Books by George Orwell:")
for book in books_by_author:
    print(book.title)

# List all books in a library
library = Library.objects.get(name="Central Library")
library_books = library.books.all()
print("\nBooks in Central Library:")
for book in library_books:
    print(book.title)

# Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)
print("\nLibrarian of Central Library:")
print(librarian.name)