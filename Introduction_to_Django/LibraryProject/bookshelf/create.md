<!-- Command to create a Book instance and result-->

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

book.save()

<!-- Confirming input -->
>>> book.title
'1984'
>>> book.author
'George Orwell'
>>> book.publication_year
1949



