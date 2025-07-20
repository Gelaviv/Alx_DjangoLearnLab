from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book

# Create your views here.
def list_books(request):
    books = Book.objects.all().select_related('author')  # Optimize query
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_queryset(self):
        return Library.objects.prefetch_related('books__author')