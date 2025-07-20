from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")

    # Create books
    book1 = Book.objects.create(title="Harry Potter 1", author=author1)
    book2 = Book.objects.create(title="Harry Potter 2", author=author1)
    book3 = Book.objects.create(title="A Game of Thrones", author=author2)
    
    # Create library
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2, book3)
    
    # Create librarian
    librarian = Librarian.objects.create(name="John Smith", library=library)

# Query 1: All books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# Query 2: All books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Query 3: Librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)

# Example usage
if __name__ == "__main__":
    
    print("Books by J.K. Rowling:")
    for book in get_books_by_author("J.K. Rowling"):
        print(book.title)
    
    print("\nBooks in Central Library:")
    for book in get_books_in_library("Central Library"):
        print(book.title)
    
    print("\nLibrarian for Central Library:")
    print(get_librarian_for_library("Central Library").name)

    