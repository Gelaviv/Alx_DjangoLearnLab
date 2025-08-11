from django.shortcuts import render
from .models import Author, Book
from rest_framework import filters
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

# Create your views here.

class BookListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """
    View for listing all books and creating new books.
    - GET: Returns list of all books (available to everyone)
    - POST: Creates a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    

      # Filtering and searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['publication_year', 'author']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # Default ordering



    def get(self, request, *args, **kwargs):
        """Handle GET requests - list all books"""
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Handle POST requests - create a new book"""
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Custom create method to add additional logic if needed"""
        serializer.save()




class BookDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """
    View for retrieving, updating, or deleting a specific book.
    - GET: Retrieve book details (available to everyone)
    - PUT/PATCH: Update book (requires authentication)
    - DELETE: Remove book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        """Handle GET requests - retrieve single book"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Handle PUT requests - full update of book"""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests - partial update of book"""
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle DELETE requests - remove book"""
        return self.destroy(request, *args, **kwargs)

class AuthorListView(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Similar implementation for Author model"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class AuthorDetailView(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    """Similar implementation for Author details"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)