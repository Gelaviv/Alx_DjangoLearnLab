<!-- Retrieving the book -->
book = Book.objects.get(title="1984")

<!--  Updating the title, saving and printing -->

book.title = "Nineteen Eighty-Four"

book.save()

print(book.title)

<!-- Expected Output -->
Nineteen Eighty-Four