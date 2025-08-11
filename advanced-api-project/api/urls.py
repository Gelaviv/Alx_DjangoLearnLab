from django.urls import path
from .views import BookListView,BookCreateView,BookUpdateView,BookDeleteView,BookDetailView,AuthorListView,AuthorCreateView,AuthorUpdateView,AuthorDeleteView,AuthorDetailView


urlpatterns = [
  # Book endpoints
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    

    path('books/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/delete/', BookDeleteView.as_view(), name='book-delete'),
    
    # Author endpoints
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
]