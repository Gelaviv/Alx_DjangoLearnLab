from bookshelf.models import Book

<!-- Retrieving the book -->
book = Book.objects.get(title="Nineteen Eighty-Four")

<!-- Deleting the book -->

book.delete()

<!-- Trying to retrieve all books -->

Book.objects.all()

<!-- Expected output -->

QuerySet []>