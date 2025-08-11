from django.shortcuts import render
from .models import Author, Book
from rest_framework import filters
from .serializers import AuthorSerializer, BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView,UpdateAPIView,DestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

# Create your views here.

class BookListView(ListCreateAPIView):
    """
    View for listing all books and creating new books.
    - GET: Returns list of all books (available to everyone)
    - POST: Creates a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    

      # Filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'publication_year', 'author__name']
    search_fields = ['title', 'author__name', 'description']
    ordering_fields = ['title', 'publication_year', 'created_at']
    ordering = ['title']  # Default ordering

    def get_queryset(self):
        """
        Optionally filters the queryset by minimum publication year
        Example: ?min_year=2000
        """
        queryset = super().get_queryset()
        min_year = self.request.query_params.get('min_year')
        if min_year:
            queryset = queryset.filter(publication_year__gte=min_year)
        return queryset

class BookCreateView(CreateAPIView):
    """
    Dedicated view for creating books (if separate from list is needed)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save()



class BookUpdateView(UpdateAPIView):
    """
    Dedicated view for updating books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self):
        # Get pk from request data instead of URL
        pk = self.request.data.get('id')
        return Book.objects.get(pk=pk)

class BookDeleteView(DestroyAPIView):
    """
    Dedicated view for deleting books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    def get_object(self):
        # Get pk from request data instead of URL
        pk = self.request.data.get('id')
        return Book.objects.get(pk=pk)

class BookDetailView(RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating or deleting a book.
    Combines DetailView, UpdateView and DeleteView.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class AuthorListView(ListCreateAPIView):
    """View for listing and creating authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class AuthorCreateView(CreateAPIView):
    """Dedicated view for creating authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]

class AuthorUpdateView(UpdateAPIView):
    """Dedicated view for updating authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class AuthorDeleteView(DestroyAPIView):
    """Dedicated view for deleting authors"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    """View for retrieving, updating or deleting an author"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]